import re
import subprocess
import gradio as gr

from ollama import Client
from ollama_manager import list_model_names, model_exists, start_model, stop_model


# --- Helpers ---
def clean_model_name(name: str) -> str:
    if not name:
        return ""

    return re.sub(r'[^a-zA-Z0-9\.:-]', '', name.strip())


def start_handler(selected_model, manual_name):
    """
    Starts the specified model in Ollama (selected or manually entered).
    Args:
        selected_model (str): Model name from dropdown.
        manual_name (str): Model name entered manually.
    Returns:
        tuple[str, gr.update]: Status message and image update (None).
    """
    use = manual_name.strip() or selected_model or ""

    if not use:
        return "⚠️ No model name provided.", None

    if not model_exists(use):
        return f"⚠️ Model '{use}' not found in Ollama.", None

    try:
        start_model(use)

        return f"✅ Model '{use}' started successfully!", None

    except Exception as e:
        return f"❌ Failed to start model '{use}': {e}", None


def stop_handler(selected_model, manual_name):
    """
    Stops the specified model in Ollama.
    Args:
        selected_model (str): Model name from dropdown.
        manual_name (str): Model name entered manually. 
    Returns:
        tuple[str, gr.update]: Status message and image update (None).
    """
    use = manual_name.strip() or selected_model or ""

    if not use:
        return "⚠️ No model name provided.", None

    try:
        if stop_model(use):
            return f"🛑 Model '{use}' stopped successfully.", None

    except Exception as e:
        return f"❌ Error stopping model '{use}': {e}", None


def refresh_handler():
    """
    Connects to Ollama and retrieves the list of installed models.
    Returns:
        tuple[gr.update, str]: Dropdown choices update and status message.
    """
    try:
        names = list_model_names()

        if not names:
            return gr.update(choices = []), "No models found or Ollama not reachable"

        return gr.update(choices = names), f"Found {len(names)} model(s)."

    except Exception as e:
        return gr.update(choices = []), f"❌ Failed to connect to Ollama: {e}"


def status_handler():
    try:
        result = subprocess.run(["ollama", "ps"], capture_output = True, text = True, timeout = 10)
        return result.stdout.strip()

    except Exception as e:
        return f"❌ Failed to get status: {e}"


def chat_handler(selected_model, manual_name, prompt):
    """
    Sends a prompt to the selected Ollama model for chat completion.
    Args:
        selected_model (str): Model name from dropdown.
        manual_name (str): Model name entered manually.
        prompt (str): User's input prompt.
    Returns:
        tuple[str, gr.update]: Model's response and cleared input field update.
    """
    use = manual_name.strip() or selected_model or ""

    if not use:
        return "⚠️ No model selected.", gr.update(value="")

    try:
        client = Client(host = "http://localhost:11434")
        response = client.generate(model = use, prompt = prompt)

        return response["response"], gr.update(value = "")

    except Exception as e:
        return f"❌ Chat failed: {e}", gr.update(value = "")


# --- Gradio UI ---
with gr.Blocks() as demo:
    gr.Markdown("""
                ## 💻🧠🖥 Ollama Control Panel

                Start, stop, check status, and chat with models.

                **⚠️ Important:**
                - Press **Refresh** to load available models.
                - If **Ollama is not running**, the list will be empty and actions will fail.
                - You must start Ollama before using this panel.

                **To stop the app, press _Ctrl+C_ in the terminal!**
                """)


    with gr.Row():
        models_dd = gr.Dropdown(choices = [], label = "Choose Ollama model")
        refresh_btn = gr.Button("🔄 Refresh models")

    with gr.Row():
        custom_input = gr.Textbox(label = "Or enter model name manually",
                                  placeholder = "e.g. mistral:7b")
        start_btn = gr.Button("▶️ Start model")
        stop_btn = gr.Button("⏹ Stop model")

    info = gr.Textbox(label = "Message", interactive = False, lines = 3)
    out_image = gr.Image(label = "(no image)", visible = False)

    status_btn = gr.Button("🔍 Show status")
    status_box = gr.Textbox(label = "Status", interactive = False, lines = 10)

    gr.Markdown("### Chat with model")
    chat_input = gr.Textbox(label = "Enter prompt", placeholder = "Ask something...")
    chat_btn = gr.Button("💬 Send prompt")
    chat_output = gr.Textbox(label = "Model response", interactive = False, lines = 10)

    # Wire buttons
    refresh_btn.click(fn = refresh_handler, inputs = None, outputs = [models_dd, info])

    start_btn.click(fn = start_handler, inputs = [models_dd, custom_input],
                    outputs = [info, out_image])

    stop_btn.click(fn = stop_handler, inputs = [models_dd, custom_input],
                   outputs = [info, out_image])

    status_btn.click(fn = status_handler, inputs = None, outputs = status_box)

    chat_btn.click(fn = chat_handler, inputs = [models_dd, custom_input, chat_input],
                    outputs = [chat_output, chat_input])


if __name__ == "__main__":
    demo.launch()

