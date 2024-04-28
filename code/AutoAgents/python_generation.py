import autogen

BASE_URL="http://localhost:11434/v1/"

#'base_url': "http://0.0.0.0:8001",
#	'model': "ollama/mistral",

# Openai Secret key 
openai_key = ""
config_list_mistral = [
    {
	'base_url': BASE_URL,
        'api_key': "NULL",
	'model': "mistral",
	'timeout': 1800
    }
]

config_list_openai = [
    {
	'base_url': "https://api.openai.com/v1",
        'api_key': openai_key,
	'model': "gpt-3.5"
    }
]

#'base_url': "http://0.0.0.0:8000",
#	'model': "ollama/llama2-uncensored",
config_list_codellama = [
    {
	'base_url': BASE_URL,
        'api_key': "NULL",
	'model': "llama2-uncensored",
	'timeout': 1800
    }
]

llm_config_mistral={
    "config_list": config_list_mistral,
}

llm_config_codellama={
    "config_list": config_list_codellama,
}

llm_config_openai={
    "config_list": config_list_openai,
}

# Start logging
logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
print("Logging session ID: " + str(logging_session_id))

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_codellama
    #llm_config=llm_config_openai
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
	"work_dir": "coding",
	"use_docker": False
    }, # IMPORTANT: set to True to run code in docker, recommended
    llm_config=llm_config_mistral,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction. Be sure to get the latest info and methodologies online and test all the code proposed. Save the proposed code in the folder coding. Keep it simple and test it.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

# Write a python script to output numbers 1 to 100 and then the user_proxy agent should run the script
#In python Write a tradebot capable of understanding the market analysing the best source you can make sense of. It should be teastable in an environment like gainium.io. You can use machine learning technique to solve the problem but I am open to your innovative ideas. Please save all your attempts in the folder web with consequtive names.
#task="""Implement a simple python application to make a crypto trading bot that takes its decision making a sentimenth analysis scraping the site coinbase.com. Do not talk to much about libraries to use but create a working prototype. Do not use any specfic coinbase APIs if not scraping the website. Keep it simple but working.
#The goal is to have a working program.
#task="""I am a new Scrum master in a pre-existing team, I have troubles to make good connections with the key figures in the team such Analyst and Delivery Manager. All my proposals are dinied because they think that their current way of working is better of my experience in the past years and that the change that I'd like to do are just time lost. How can I make them understand my point of view and the value of my propositions.
#I am also lacking the support of my manager. Define come clear points on how can I improve my working relation ship with them.

#task="""I'll give you an array of dictionary like this: [{"crypto": "ethereum", "date": "2023-11-23", "sentiment": [80, 10, 10]}, {"crypto": "bitcoin", "date": "2023-02-26", "sentiment": [10, 30, 60]}]. The sentiment is respectively positive, negative and netutral. I need a python script that will be trained daily, or more frequently ,and that will predict the sentiment in the next days. I need distinct functions to train the ML model and predict the outcome. Create also a json file with some test data based on the example given. The training data must be read from a file; json or better as you think is better.

task="""I want to do a video presentation on ollama and pyautogen software. Think on the most imprtant things to share and create a detailed plan on what to share and how much time to spend. The total video time must under 20 minutes. I'll spend around 5mins in a real demo.
Serach in internet for the latest information and propose the 3 best use-cases. Create a markdown presentation.
"""

chat_res = user_proxy.initiate_chat(
	coder,
	message=task,
	summary_method="reflection_with_llm",
)

autogen.runtime_logging.stop()

# Some output
print("Chat history:", chat_res.chat_history)
print("Summary:", chat_res.summary)
print("Cost info:", chat_res.cost)

# Improve output reading from sqlite https://microsoft.github.io/autogen/docs/notebooks/agentchat_logging#getting-data-from-the-sqlite-database
