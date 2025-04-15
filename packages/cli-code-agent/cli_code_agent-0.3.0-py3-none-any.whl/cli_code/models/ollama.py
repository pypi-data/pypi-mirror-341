import glob
import json  # For formatting tool results
import logging
import os
from typing import Dict, List

import questionary  # Import questionary
from rich.console import Console
from rich.panel import Panel  # Import Panel

# Attempt to import the OpenAI client library
try:
    import openai
    from openai import OpenAI  # Import the client class
except ImportError:
    # This allows the module to be imported even if openai isn't installed yet,
    # but methods using it will fail later if it's not installed.
    openai = None
    OpenAI = None
    # Log a warning or raise a more specific error during __init__ if openai is None.
    pass

from ..tools import AVAILABLE_TOOLS, get_tool  # Import get_tool
from ..utils import count_tokens  # Import count_tokens
from .base import AbstractModelAgent

# Import MessageToDict for schema conversion
try:
    from google.protobuf.json_format import MessageToDict
except ImportError:
    MessageToDict = None  # Handle missing dependency gracefully

log = logging.getLogger(__name__)
MAX_OLLAMA_ITERATIONS = 5  # Limit tool call loops for Ollama initially
SENSITIVE_TOOLS = ["edit", "create_file"]  # Define sensitive tools requiring confirmation
OLLAMA_MAX_CONTEXT_TOKENS = 80000  # Example token limit for Ollama models, adjust as needed


class OllamaModel(AbstractModelAgent):
    """Interface for Ollama models using the OpenAI-compatible API."""

    def __init__(self, api_url: str, console: Console, model_name: str | None = None):
        """Initialize the Ollama model interface."""
        super().__init__(console=console, model_name=model_name)  # Call base class init

        if not OpenAI:
            log.error("OpenAI client library not found. Please install it: pip install openai")
            raise ImportError(
                "OpenAI client library is required for the Ollama provider. Please run: pip install openai"
            )

        if not api_url:
            raise ValueError("Ollama API URL (base_url) is required.")

        self.api_url = api_url
        # self.model_name is set by super().__init__
        # The actual default model name from config should be resolved in main.py before passing

        try:
            # Initialize OpenAI client pointing to the Ollama base URL
            # Use a placeholder API key as Ollama doesn't require one by default
            self.client = OpenAI(
                base_url=self.api_url,
                api_key="ollama",  # Required by the openai client, but value doesn't matter for Ollama
            )
            log.info(f"OpenAI client initialized for Ollama at: {self.api_url}")
            # Optionally, add a quick ping or model list check here to verify connection
            # self.list_models() # Could do a quick check
        except Exception as e:
            log.error(f"Failed to initialize OpenAI client for Ollama at {self.api_url}: {e}", exc_info=True)
            raise ConnectionError(f"Could not connect to Ollama API at {self.api_url}: {e}") from e

        # TODO: Add Ollama-specific tool/function calling setup if different from OpenAI standard
        # self.ollama_tools = self._prepare_ollama_tools()

        # --- Initialize Ollama-specific History & System Prompt ---
        self.history = []
        # Define the system prompt
        self.system_prompt = (
            "You are a helpful AI coding assistant. You have access to a set of tools to interact with the local file system "
            "and execute commands. \n\n"
            "**CRITICAL:** When you decide to use a tool, you **MUST** provide **ALL** required arguments for that tool. "
            "Check the tool's definition for its required parameters (like 'file_path', 'pattern', 'content', etc.) and ensure you include them in your request. "
            "Failure to provide required arguments will result in an error.\n\n"
            "**IMPORTANT CONTEXT INFORMATION:** Your context about this project comes from the .rules/*.md files (specifically "
            ".rules/context.md and .rules/tools.md). If asked about context, refer to these files using their full paths with '.rules/' prefix. "
            "Do not try to access 'context.md' directly in the root directory.\n\n"
            "Use the available tools when necessary to fulfill the user's request. "
            "Think step-by-step if needed. "
            "If you need to see the content of a file before editing, use the 'view' tool first (providing the 'file_path'). "
            "If a file is large, consider using 'summarize_code' or viewing specific sections with 'view' offset/limit (always provide 'file_path'). "
            "After performing actions, confirm the outcome or provide a summary."
            # TODO: Potentially add details about specific tool usage or desired output format.
        )
        # Add system prompt as the first message
        self.add_to_history({"role": "system", "content": self.system_prompt})
        log.info(f"OllamaModel initialized for endpoint {self.api_url} with system prompt.")

    def _get_initial_context(self) -> str:
        """
        Gets the initial context for the conversation based on the following hierarchy:
        1. Content of .rules/*.md files if the directory exists
        2. Content of README.md in the root directory if it exists
        3. Output of 'ls' command (fallback to original behavior)

        Returns:
            A string containing the initial context.
        """

        # Check if .rules directory exists
        if os.path.isdir(".rules"):
            log.info("Found .rules directory. Reading *.md files for initial context.")
            try:
                md_files = glob.glob(".rules/*.md")
                if md_files:
                    context_content = []
                    for md_file in md_files:
                        log.info(f"Reading rules file: {md_file}")
                        try:
                            with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read().strip()
                                if content:
                                    file_basename = os.path.basename(md_file)
                                    context_content.append(f"# Content from {file_basename}\n\n{content}")
                        except Exception as read_err:
                            log.error(f"Error reading rules file '{md_file}': {read_err}", exc_info=True)

                    if context_content:
                        combined_content = "\n\n".join(context_content)
                        self.console.print("[dim]Context initialized from .rules/*.md files.[/dim]")
                        return f"Project rules and guidelines:\n```markdown\n{combined_content}\n```\n"
            except Exception as rules_err:
                log.error(f"Error processing .rules directory: {rules_err}", exc_info=True)

        # Check if README.md exists in the root
        if os.path.isfile("README.md"):
            log.info("Using README.md for initial context.")
            try:
                with open("README.md", "r", encoding="utf-8", errors="ignore") as f:
                    readme_content = f.read().strip()
                if readme_content:
                    self.console.print("[dim]Context initialized from README.md.[/dim]")
                    return f"Project README:\n```markdown\n{readme_content}\n```\n"
            except Exception as readme_err:
                log.error(f"Error reading README.md: {readme_err}", exc_info=True)

        # Fall back to ls output (original behavior)
        log.info("Falling back to 'ls' output for initial context.")
        try:
            ls_tool = get_tool("ls")
            if ls_tool:
                ls_result = ls_tool.execute()
                log.info(f"Orientation ls result length: {len(ls_result) if ls_result else 0}")
                self.console.print("[dim]Directory context acquired via 'ls'.[/dim]")
                return f"Current directory contents (from initial `ls`):\n```\n{ls_result}\n```\n"
            else:
                log.error("CRITICAL: Could not find 'ls' tool for mandatory orientation.")
                # Stop execution if ls tool is missing - fundamental context is unavailable
                return "Error: The essential 'ls' tool is missing. Cannot proceed."
        except Exception as orient_error:
            log.error(f"Error during mandatory orientation (ls): {orient_error}", exc_info=True)
            error_message = f"Error during initial directory scan: {orient_error}"
            self.console.print(f"[bold red]Error getting initial directory listing: {orient_error}[/bold red]")
            # Stop execution if initial ls fails - context is unreliable
            return f"Error: Failed to get initial directory listing. Cannot reliably proceed. Details: {orient_error}"

    def generate(self, prompt: str) -> str | None:
        """Generate a response using the Ollama model via OpenAI API format."""
        if not self.client:
            log.error("Ollama generate called but OpenAI client not initialized.")
            return "Error: Ollama client not initialized."

        # Ensure model name is set (either from constructor or config default resolved in main)
        if not self.model_name:
            log.error("Ollama generate called without a model name specified.")
            return "Error: No Ollama model name configured or specified."

        log.info(f"Ollama Agent Loop - Processing prompt: '{prompt[:100]}...' using model '{self.model_name}'")

        # === Step 1: Get Initial Context ===
        orientation_context = self._get_initial_context()

        # Combine orientation with the actual user request
        full_prompt = f"{orientation_context}\nUser request: {prompt}"

        # Add the enriched prompt to history
        self.add_to_history({"role": "user", "content": full_prompt})
        log.debug(f"Prepared full prompt:\n---\n{full_prompt}\n---")

        iteration_count = 0
        final_response = None
        while iteration_count < MAX_OLLAMA_ITERATIONS:
            iteration_count += 1
            log.info(f"Ollama Agent Iteration {iteration_count}/{MAX_OLLAMA_ITERATIONS}")

            try:
                # === Prepare Tools for API Call ===
                # Convert our tool schemas to OpenAI format
                current_tools = self._prepare_openai_tools()

                # === Call Ollama (OpenAI API) ===
                log.debug(
                    f"Sending request to Ollama. Model: {self.model_name}. History: {self.history}. Tools: {current_tools}"
                )
                with self.console.status(f"[yellow]Ollama thinking ({self.model_name})...", spinner="dots"):
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=self.history,
                        tools=current_tools,
                        tool_choice="auto",  # Let the model decide if it needs tools
                        # Add other parameters like temperature if needed
                    )
                log.debug(f"Raw Ollama Response (Iter {iteration_count}): {response}")

                response_message = response.choices[0].message

                # === Handle Response ===
                tool_calls = response_message.tool_calls
                if tool_calls:
                    # === Tool Call Requested ===
                    log.info(f"Ollama requested {len(tool_calls)} tool call(s).")
                    # Add the assistant's response (containing the tool requests) to history
                    self.add_to_history(response_message.model_dump(exclude_unset=True))

                    # --- Execute Tools (with HITL) ---
                    for tool_call in tool_calls:
                        tool_name = tool_call.function.name
                        tool_args_str = tool_call.function.arguments
                        tool_call_id = tool_call.id
                        log.info(f"Processing tool call: ID={tool_call_id}, Name={tool_name}, Args='{tool_args_str}'")

                        # Special handling for task_complete tool to extract the final response
                        if tool_name == "task_complete":
                            try:
                                tool_args = json.loads(tool_args_str)
                                summary = tool_args.get("summary", "Task completed successfully.")
                                final_response = summary
                                log.info(f"Task completion tool called with summary: {summary}")

                                # Add the response to history for context
                                self.add_to_history(
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call_id,
                                        "name": tool_name,
                                        "content": summary,
                                    }
                                )

                                # Return the summary directly instead of the JSON
                                return final_response
                            except json.JSONDecodeError:
                                log.error(f"Failed to decode JSON for task_complete: {tool_args_str}")
                                continue

                        tool_result = ""
                        tool_error = False
                        user_rejected = False  # Flag for confirmation

                        try:
                            tool_args = json.loads(tool_args_str)
                        except json.JSONDecodeError:
                            log.error(f"Failed to decode JSON arguments for tool {tool_name}: {tool_args_str}")
                            tool_result = f"Error: Invalid JSON arguments provided: {tool_args_str}"
                        else:
                            # --- HUMAN IN THE LOOP CONFIRMATION ---
                            if tool_name in SENSITIVE_TOOLS:
                                file_path = tool_args.get("file_path", "(unknown file)")
                                content = tool_args.get("content")
                                old_string = tool_args.get("old_string")
                                new_string = tool_args.get("new_string")

                                panel_content = f"[bold yellow]Proposed Action:[/bold yellow]\n[cyan]Tool:[/cyan] {tool_name}\n[cyan]File:[/cyan] {file_path}\n"

                                if content is not None:
                                    preview_lines = content.splitlines()[:10]  # Show first 10 lines
                                    preview = "\n".join(preview_lines)
                                    if len(content.splitlines()) > 10:
                                        preview += "\n... (truncated)"
                                    action_desc = f"Write/Overwrite with content:\n---\n{preview}\n---"
                                elif old_string is not None and new_string is not None:
                                    action_desc = (
                                        f"Replace first occurrence of:\n '{old_string}'\nWith:\n '{new_string}'"
                                    )
                                elif (
                                    content is None and old_string is None and new_string is None
                                ):  # Handle empty file creation explicitly if needed
                                    action_desc = "Create empty file (or clear existing)."
                                else:
                                    action_desc = "(Could not determine specific change)"

                                panel_content += f"[cyan]Change:[/cyan]\n{action_desc}"

                                self.console.print(
                                    Panel(
                                        panel_content, title="Confirmation Required", border_style="red", expand=False
                                    )
                                )
                                try:
                                    user_confirmed = questionary.confirm(
                                        "Proceed with this action?",
                                        default=False,
                                        auto_enter=False,
                                    ).ask()
                                except KeyboardInterrupt:  # Handle Ctrl+C during question
                                    user_confirmed = False
                                    self.console.print("[yellow]Action cancelled by user.[/yellow]")

                                if not user_confirmed:
                                    log.warning(f"User rejected execution of sensitive tool: {tool_name}")
                                    user_rejected = True
                                    tool_result = (
                                        f"User rejected the execution of tool '{tool_name}' on file '{file_path}'."
                                    )
                                    tool_error = True  # Treat rejection as an error for the LLM's perspective
                            # --- END HITL ---

                            # --- Execute the actual tool (only if not rejected) ---
                            if not user_rejected:
                                tool_instance = get_tool(tool_name)
                                if tool_instance:
                                    try:
                                        # --- Generalized Check for Required Arguments ---
                                        declaration = tool_instance.get_function_declaration()
                                        required_params = []
                                        if (
                                            declaration
                                            and declaration.parameters
                                            and declaration.parameters._pb
                                            and MessageToDict
                                        ):
                                            try:
                                                # Convert the protobuf Schema to a dict to check 'required'
                                                parameters_dict = MessageToDict(declaration.parameters._pb)
                                                required_params = parameters_dict.get("required", [])
                                            except Exception as conversion_err:
                                                log.warning(
                                                    f"Failed to convert parameters schema to dict for checking required args for tool '{tool_name}': {conversion_err}"
                                                )
                                                # Proceed without check if conversion fails? Or raise?
                                                # For now, log warning and assume no required params checked.

                                        missing_args = []
                                        for param in required_params:
                                            if param not in tool_args:
                                                missing_args.append(param)

                                        if missing_args:
                                            log.error(
                                                f"Ollama requested {tool_name} but missing required args: {missing_args}. Provided: {tool_args}"
                                            )
                                            raise ValueError(
                                                f"Missing required arguments for tool '{tool_name}': {', '.join(missing_args)}"
                                            )
                                        # --- End Check ---

                                        with self.console.status(
                                            f"[cyan]Executing tool: {tool_name}...", spinner="dots"
                                        ):
                                            tool_result = tool_instance.execute(**tool_args)
                                        log.info(
                                            f"Tool {tool_name} executed successfully. Result length: {len(tool_result) if tool_result else 0}"
                                        )
                                        tool_error = False
                                    except Exception as tool_exec_error:
                                        log.error(
                                            f"Error executing tool {tool_name} with args {tool_args}: {tool_exec_error}",
                                            exc_info=True,
                                        )
                                        tool_result = f"Error executing tool {tool_name}: {str(tool_exec_error)}"
                                        tool_error = True
                                else:
                                    log.error(f"Tool '{tool_name}' requested by Ollama not found in available tools.")
                                    tool_result = f"Error: Tool '{tool_name}' not found."
                                    tool_error = True

                        # --- Add Tool Result to History ---
                        # (This happens regardless of user_rejected because we need to inform the LLM)
                        self.add_to_history(
                            {
                                "tool_call_id": tool_call_id,
                                "role": "tool",
                                "name": tool_name,
                                "content": tool_result,  # Send back execution result OR rejection message
                            }
                        )
                    # --- Loop back to LLM ---
                    continue  # Continue the while loop to send tool results back to Ollama

                else:
                    # Handle standard text responses that don't use tools
                    content = response_message.content
                    if content:
                        # Add the response to history
                        self.add_to_history(response_message.model_dump(exclude_unset=True))
                        log.info(f"Received direct text response (no tool calls), length: {len(content)}")
                        # Return the actual text response
                        return content
                    else:
                        log.warning("Received empty content from model response with no tool calls")
                        return "The model provided an empty response. Please try again with a more specific question."

            except Exception as e:
                log.error(f"Error during Ollama agent iteration {iteration_count}: {e}", exc_info=True)
                self.console.print(f"[bold red]Error during Ollama interaction:[/bold red] {e}")
                # Clean history? Pop last user message?
                if self.history and self.history[-1].get("role") == "user":
                    self.history.pop()
                return f"(Error interacting with Ollama: {e})"  # Return error message

        # If loop finishes without returning text (e.g., max iterations)
        log.warning(f"Ollama agent loop reached max iterations ({MAX_OLLAMA_ITERATIONS}).")
        return "(Agent reached maximum iterations)"

    def list_models(self) -> List[Dict] | None:
        """
        List available models from the configured Ollama endpoint.
        """
        log.info(f"Attempting to list models from Ollama endpoint: {self.api_url}")
        if not self.client:
            log.error("OpenAI client not initialized for Ollama.")
            return None
        try:
            models_response = self.client.models.list()
            # The response object is a SyncPage[Model], access data via .data
            available_models = []
            for model in models_response.data:
                # Adapt the OpenAI Model object to our expected dict format
                model_info = {
                    "id": model.id,  # Typically the model identifier used in API calls
                    "name": getattr(model, "name", model.id),  # Use name if available, else id
                    # Add other potentially useful fields if needed, e.g., owner
                    # "owned_by": model.owned_by
                }
                available_models.append(model_info)
            log.info(f"Found {len(available_models)} models at {self.api_url}")
            return available_models
        except Exception as e:
            log.error(f"Error listing models from Ollama at {self.api_url}: {e}", exc_info=True)
            self.console.print(f"[bold red]Error contacting Ollama endpoint '{self.api_url}':[/bold red] {e}")
            self.console.print("[yellow]Ensure the Ollama server is running and the API URL is correct.[/yellow]")
            return None  # Indicate failure

    # TODO: Add helper methods for tool schema conversion, history formatting etc.
    # def _prepare_ollama_tools(self):
    #     ...

    # --- Ollama-specific history management ---
    def add_to_history(self, message: Dict):
        """Adds a message dictionary (OpenAI format) to the history and manages context window."""
        if not isinstance(message, dict) or "role" not in message:
            log.warning(f"Attempted to add invalid message to Ollama history: {message}")
            return
        self.history.append(message)
        self._manage_ollama_context()  # Call context management after adding

    def clear_history(self):
        """Clears the Ollama conversation history, preserving the system prompt."""
        # Save the system prompt if it exists
        system_prompt = None
        if self.history and self.history[0].get("role") == "system":
            system_prompt = self.history[0]["content"]

        # Clear the history
        self.history = []

        # Re-add system prompt after clearing if it exists
        if system_prompt:
            self.history.insert(0, {"role": "system", "content": system_prompt})
            log.info("Ollama history cleared, system prompt preserved.")
        else:
            log.info("Ollama history cleared completely.")

    def _manage_ollama_context(self):
        """Truncates Ollama history based on estimated token count."""
        # If history is empty or has just one message (system prompt), no need to truncate
        if len(self.history) <= 1:
            return

        # Separate system prompt (must be kept)
        system_message = None
        current_history = list(self.history)  # Work on a copy
        if current_history and current_history[0].get("role") == "system":
            system_message = current_history.pop(0)

        # Calculate initial token count (excluding system prompt for removal logic)
        total_tokens = 0
        for message in ([system_message] if system_message else []) + current_history:
            try:
                message_str = json.dumps(message)
                total_tokens += count_tokens(message_str)
            except TypeError as e:
                log.warning(f"Could not serialize message for token counting: {message} - Error: {e}")
                total_tokens += len(str(message)) // 4

        log.debug(f"Estimated total tokens before truncation: {total_tokens}")

        if total_tokens <= OLLAMA_MAX_CONTEXT_TOKENS:
            return  # No truncation needed

        log.warning(
            f"Ollama history token count ({total_tokens}) exceeds limit ({OLLAMA_MAX_CONTEXT_TOKENS}). Truncating."
        )

        # Keep removing the oldest messages (after system prompt) until under limit
        messages_removed = 0
        initial_length_before_trunc = len(current_history)  # Length excluding system prompt
        while total_tokens > OLLAMA_MAX_CONTEXT_TOKENS and len(current_history) > 0:
            removed_message = current_history.pop(0)  # Remove from the beginning (oldest)
            messages_removed += 1
            try:
                removed_tokens = count_tokens(json.dumps(removed_message))
            except TypeError:
                removed_tokens = len(str(removed_message)) // 4
            total_tokens -= removed_tokens
            log.debug(f"Removed message ({removed_tokens} tokens). New total: {total_tokens}")

        # Reconstruct the final history
        final_history = []
        if system_message:
            final_history.append(system_message)
        final_history.extend(current_history)  # Add the remaining (truncated) messages

        # Update the model's history
        original_total_length = len(self.history)
        self.history = final_history
        final_total_length = len(self.history)

        log.info(
            f"Ollama history truncated from {original_total_length} to {final_total_length} messages ({messages_removed} removed)."
        )

    # --- Tool Preparation Helper ---
    def _prepare_openai_tools(self) -> List[Dict] | None:
        """Converts available tools to the OpenAI tool format."""
        if not AVAILABLE_TOOLS:
            return None

        if not MessageToDict:
            log.error(
                "google.protobuf library is required for tool schema conversion. Please install it: pip install protobuf"
            )
            # Or raise ImportError here
            return None  # Cannot prepare tools without the library

        openai_tools = []
        for name, tool_instance in AVAILABLE_TOOLS.items():
            try:
                declaration = tool_instance.get_function_declaration()
                if declaration and declaration.parameters:
                    # --- FIX: Convert Schema object to Dict using MessageToDict ---
                    try:
                        # The declaration.parameters object should be a protobuf Message
                        parameters_dict = MessageToDict(
                            declaration.parameters._pb
                        )  # Access the underlying protobuf message (_pb)
                        # Optional: Clean empty fields if MessageToDict includes them explicitly
                        # parameters_dict = {k: v for k, v in parameters_dict.items() if v}
                    except Exception as conversion_err:
                        log.error(
                            f"Failed to convert parameters schema for tool '{name}' using MessageToDict: {conversion_err}",
                            exc_info=True,
                        )
                        continue  # Skip this tool if conversion fails
                    # --- END FIX ---

                    tool_dict = {
                        "type": "function",
                        "function": {
                            "name": declaration.name,
                            "description": declaration.description,
                            "parameters": parameters_dict,  # Use the converted dictionary
                        },
                    }
                    openai_tools.append(tool_dict)
                elif declaration:  # Handle case with no parameters
                    tool_dict = {
                        "type": "function",
                        "function": {
                            "name": declaration.name,
                            "description": declaration.description,
                        },
                    }
                    openai_tools.append(tool_dict)
                else:
                    log.warning(f"Could not get function declaration for tool '{name}'. Skipping.")

            except Exception as e:
                log.error(f"Error preparing tool '{name}' for OpenAI format: {e}", exc_info=True)

        log.debug(f"Prepared {len(openai_tools)} tools for Ollama API call.")
        return openai_tools if openai_tools else None
