import autogen

config_list = [
    {
        "api_base": "http://127.0.0.1:8000",
        "api_key" : "NULL",
    }
]

llm_config = {
    "request_timeout" : 800,
    "config_list" : config_list
}

assistant = autogen.AssistantAgent(
    "assistant",
    llm_config = llm_config
)

user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    code_execution_config = {
        "work_dir" : "coding"
    }
)

user_proxy.initiate_chat(
    assistant,
    message ="What is the name of the model you are based on?"
)

