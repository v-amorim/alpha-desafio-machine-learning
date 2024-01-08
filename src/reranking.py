from __future__ import annotations

import os

import cohere
from dotenv import load_dotenv

load_dotenv()


# Access the API key using the environment variable
api_key = os.getenv('COHERE_API_KEY')

co = cohere.Client(api_key)
file_path = 'skill_gem_data/skill_gem_info_treated.txt'

with open(file_path, encoding='utf-8') as file:
    file_content = file.read()

skill_gem_entries = file_content.split('\n')

skill_gem_list = [entry.strip() for entry in skill_gem_entries if entry.strip()]


def rerank(query: str) -> list[str]:
    results = co.rerank(query=query, documents=skill_gem_list, top_n=5, model='rerank-multilingual-v2.0')
    return [f"Skill Gem: {result.document['text']}; Index: {result.index}; Relevance Score: {result.relevance_score}"
            for result in results]
