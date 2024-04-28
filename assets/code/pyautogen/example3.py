import autogen

# This is the default base url for OLLAMA API
BASE_URL="http://localhost:11434/v1/"

# Configuration for the Mistral model
config_list_mistral = [
    {
	'base_url': BASE_URL,
    'api_key': "NULL",
	'model': "mistral",
	'timeout': 1800
    }
]

# Configuration for the LLama3 model
config_list_codellama = [
    {
	'base_url': BASE_URL,
        'api_key': "NULL",
	'model': "llama3:8b",
	'timeout': 1800
    }
]

# Create the LLM configuration data structure for the Mistrall LLM
llm_config_mistral={
    "config_list": config_list_mistral,
}

# Create the LLM configuration data structure for the LLama3 LLM
llm_config_codellama={
    "config_list": config_list_codellama,
}

# Start logging
logging_session_id = autogen.runtime_logging.start(config={"dbname": "example3_logs.db"})
print("Logging session ID: " + str(logging_session_id))

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_codellama
    #llm_config=llm_config_openai
)


termination_notice = """
    Do not show appreciation in your responses, say only what is necessary.
    if "Thank you" or "You\'re welcome" are said in the conversation, then say TERMINATE 
    to indicate the conversation is finished and this is your last message.
"""
system_message="""Reply TERMINATE if the task has been solved at full satisfaction. Be sure to get the latest info and methodologies online and test all the code proposed. Save the proposed code in the folder coding. Keep it simple and test it.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""

system_message += termination_notice


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
    system_message=system_message
)

# Write a python script to output numbers 1 to 100 and then the user_proxy agent should run the script
#In python Write a tradebot capable of understanding the market analysing the best source you can make sense of. It should be teastable in an environment like gainium.io. You can use machine learning technique to solve the problem but I am open to your innovative ideas. Please save all your attempts in the folder web with consequtive names.

#task="""Implement a simple python application to make a crypto trading bot that takes its decision making a sentimenth analysis scraping the site coinbase.com. Do not talk to much about libraries to use but create a working prototype. Do not use any specfic coinbase APIs if not scraping the website. Keep it simple but working.
#The goal is to have a working program.

#task="""I am a new Scrum master in a pre-existing team, I have troubles to make good connections with the key figures in the team such Analyst and Delivery Manager. All my proposals are dinied because they think that their current way of working is better of my experience in the past years and that the change that I'd like to do are just time lost. How can I make them understand my point of view and the value of my propositions.
#I am also lacking the support of my manager. Define come clear points on how can I improve my working relation ship with them.

#task="""I'll give you an array of dictionary like this: [{"crypto": "ethereum", "date": "2023-11-23", "sentiment": [80, 10, 10]}, {"crypto": "bitcoin", "date": "2023-02-26", "sentiment": [10, 30, 60]}]. The sentiment is respectively positive, negative and netutral. I need a python script that will be trained daily, or more frequently ,and that will predict the sentiment in the next days. I need distinct functions to train the ML model and predict the outcome. Create also a json file with some test data based on the example given. The training data must be read from a file; json or better as you think is better.

task="""#filename: coding/example3_generated_code.py
Start from scratch.
Save all the code proposals adding the suffix -v1, -v2, -v3, etc. to the file name.
Create a Python script that will execute the follow tasks:
- find all the files installed via apt or dpkg.
- check the md5sum of the installed files and compare it with what reported by the dpkg database.
- report the package name, file name, current size, new size, and modification time for each file that deviated from the original configuration.
- The script should work without passing any parameters and check all the installed packages. 
- If one parameter is passed, it would check only the specified package.
- test the script and be sure that it is working as expected for the 2 different cases: all packages and one package that you can choose between the installed ones.
- The output shoult be printed in the console. If no differences are found, print "No differences found" for every package checked.
- write the proposed code in the coding folder in the file example3_generated_code.py.
"""

chat_res = user_proxy.initiate_chat(
	coder,
	message=task,
	summary_method="reflection_with_llm",
  clear_history=True
)

autogen.runtime_logging.stop()

# Some output
#print("Chat history:", chat_res.chat_history) # All the chat history. Very verbose

print("Logging session ID: " + str(logging_session_id))
print("Summary:", chat_res.summary)
print("Cost info:", chat_res.cost)

# Improve output reading from sqlite https://microsoft.github.io/autogen/docs/notebooks/agentchat_logging#getting-data-from-the-sqlite-database
