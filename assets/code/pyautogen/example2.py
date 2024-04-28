import autogen

# This is the default base url for OLLAMA API
BASE_URL="http://localhost:11434/v1/"

# Configuration for the Mistral model
config_list = [
    {
        "base_url": BASE_URL,
        "api_key" : "NULL", # This is not needed because the model is running locally
        'model': "mistral",
	    'timeout': 1800
    }
]
# Configuration for the LLM
llm_config = {
    "timeout" : 800,
    "config_list" : config_list
}

# Create an assistant agent
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config = llm_config
)

# Create a user proxy agent - This is doing the person's job
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=30,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
	    "work_dir": "coding",
	    "use_docker": False
    }, # IMPORTANT: set to True to run code in docker, recommended
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction. Be sure to get the latest info and methodologies online and test all the code proposed. Save the proposed code in the folder coding. Keep it simple and test it.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)


task="""Find all the files installed via apt or dpkg that deviated from the original configuration. The script should output the package name, file name, current size, and new size and modification time. The script should be able to run on a linux machine. Be sure to test the script. Save the proposed code in the folder coding.  The script should work without passing any parameters and checking for all the installed packaged. If one paramater is passed, it would be the package to check. Retrieve the file list for every package from the dpkg database. Keep it simple and test the script and be sure that is working as expected.
"""

chat_res = user_proxy.initiate_chat(
	coder,
	message=task,
	summary_method="reflection_with_llm",
)