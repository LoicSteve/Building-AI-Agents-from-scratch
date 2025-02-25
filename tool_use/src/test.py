# You can test your agent and functions in this file.
from main import main



# Test cases
queries = [
    "What of next companies: Google, Apple, Microsoft has the biggest stock price?",
    "How many people live in France?",
    "What's the weather like in Berlin?",
    "I am traveling to Japan from Serbia, I have 1500 of local currency, how much of Japanese currency will I be able to get and What's the weather like in Japan? ",
    "What is the capital of France?",
    "Convert 100 USD to EUR",
    "I'm traveling to Tokyo next week. Can you tell me what the weather will be like there and also convert 200 USD to Japanese currency?",
]

# Run the agent for each query
for query in queries:
    print(f"User Query: {query}")
    response = main(query)
    print(f"Agent Response: {response}\n")