from __future__ import annotations

import os

import cohere
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key using the environment variable
api_key = os.getenv('API_KEY')

# Now, you can use the api_key variable in your code
co = cohere.Client(api_key)
file_path = 'skill_gem_data/skill_gem_info_treated.txt'

# Open the file and read its content
with open(file_path, encoding='utf-8') as file:
    file_content = file.read()

# Split the content into skill gem entries
skill_gem_entries = file_content.split('\n')

# Create a list of strings
skill_gem_list = [entry.strip() for entry in skill_gem_entries if entry.strip()]
print('Input your query: ', end='')
query = input()
# query = "Which skill gem should I use if I like Minions?"

# Rerank the list of skill gems based on the query
results = co.rerank(query=query, documents=skill_gem_list, top_n=5, model='rerank-multilingual-v2.0')

# Print the Cohere reranking results
print('Cohere Reranking Results:', results)
