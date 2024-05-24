import autogen

# This is the default base url for OLLAMA API
BASE_URL="https://api.groq.com/openai/v1"

# Configuration for the Mistral model
config_list = [
    {
        "base_url": BASE_URL,
        "api_key" : "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", # This is not needed because the model is running locally
        'model': "llama3-70b-8192",
	    'timeout': 1800
    }
]
# Configuration for the LLM
llm_config = {
    "timeout" : 800,
    "config_list" : config_list
}

# Create an assistant agent
assistant = autogen.AssistantAgent(
    "assistant",
    llm_config = llm_config
)

# Create a user proxy agent - This is doing the person's job
user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    code_execution_config = {
        "work_dir" : "coding",
        "use_docker": False
    },
)

# Start a chat with the assistant
user_proxy.initiate_chat(
    assistant,
    message = "What is the name of the model you are based on?"
    # message ="Create a python script to find all the files that deviated from the original configuration?"
)

