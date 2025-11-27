import datetime
import traceback

import gradio as gr

from autogen import ConversableAgent, AssistantAgent

# Configs we want to test
llm_config_writer = {"model" : "gemma2:2b"}
llm_config_executor = None

def test_agent_configs(writer_cfg = None, executor_cfg = None):
    """
    Create agents with the provided configs and send a short,
    safe initiating message. Returns (status_message, error_trace_or_empty).
    """
    try:
        # 1) Check if we can instantiate the AssistantAgent (writer)
        writer = AssistantAgent(
                                name = "test_writer",
                                llm_config = writer_cfg,
                                code_execution_config = False,
                                human_input_mode = "NEVER",
                                )

        # 2) Check if we can instantiate the ConversableAgent (executor)
        executor = ConversableAgent(
                                    name = "test_executor",
                                    llm_config = False,
                                    # typically the executor uses a local executor; keep False
                                    code_execution_config = False,
                                    human_input_mode = "ALWAYS",
                                    default_auto_reply = ("Please continue. If everything is "
                                                            "done, reply 'TERMINATE'."),
                                    )

        # 3) Send a minimal message to validate the chat initiation process.
        today = datetime.datetime.now().date()
        message = f"Today is {today}. Please reply briefly 'OK' for a quick config test."

        # initiate_chat may call the LLM backend depending on AutoGen internals;
        # this will expose errors related to llm_config format/initialization.
        chat_result = executor.initiate_chat(writer, message = message)

        # If it reaches this point, instantiation and initiation succeeded
        return (
                "✅ Agents instantiated and initiate_chat completed (check logs for details).",
                ""
                )

    except Exception as exc:
        tb = traceback.format_exc()

        return (
                "❌ Test failed during agent instantiation or initiate_chat. See trace below.",
                tb
                )

# --- Gradio interface for quick local testing ---
with gr.Blocks() as demo:
    gr.Markdown("### Quick AutoGen + Ollama config smoke-test\nPress the button to test only the " \
                "agent setup and a minimal initiate_chat call.")
    btn = gr.Button("Run config test")
    out_text = gr.Textbox(label = "Result", interactive = False, lines = 3)
    out_trace = gr.Textbox(label = "Trace (if any)", interactive = False, lines = 12)

    btn.click(fn = test_agent_configs, inputs = None, outputs = [out_text, out_trace])


if __name__ == "__main__":
    demo.launch()
