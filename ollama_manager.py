import subprocess

from ollama import Client


def model_exists(model_name):
    client = Client(host = 'http://localhost:11434')
    models = client.list()['models']

    return any(getattr(m, 'model', None) == model_name for m in models)


def list_model_names():
    client = Client(host = 'http://localhost:11434')
    models = client.list()['models']

    return [m.model for m in models]


def start_model(model_name = "mistral:7b"):
    """Start the Ollama model if not already running."""
    try:
        # Ollama models are loaded on-demand, so just check if the server is running
        client = Client(host = 'http://localhost:11434')
        client.generate(model = model_name, prompt = "Test")
        print(f"Model {model_name} is ready!")

    except Exception as e:
        print(f"Error starting model {model_name}: {e}")
        raise


def stop_model():
    """Stop the Ollama server (optional)."""
    # Ollama usually runs as a service, so stopping is not always needed
    # But you can stop the service if you want
    pass


if __name__ == "__main__":
    start_model("phi3.5:3.8b")
    model_exists("phi3.5:3.8b")
    list_model_names()
