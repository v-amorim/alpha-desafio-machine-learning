from __future__ import annotations

import os

import requests
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

COHERE_API_URL = 'https://api.cohere.ai/v1/rerank'
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'


def get_cohere_reranking(query, documents, top_n=5):
    headers = {
        'Authorization': f'Bearer {COHERE_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'query': query,
        'documents': documents,
        'top_n': top_n,
        'model': 'rerank-multilingual-v2.0',
    }
    response = requests.post(COHERE_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def get_chatgpt_response(prompt):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt},
        ],
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()


file_path = 'skill_gem_data/skill_gem_info_treated.txt'

with open(file_path, encoding='utf-8') as file:
    file_content = file.read()


skill_gem_entries = file_content.split('\n')


skill_gem_list = [entry.strip() for entry in skill_gem_entries if entry.strip()]


def rerank(query: str) -> list[str]:
    results = get_cohere_reranking(query=query, documents=skill_gem_list, top_n=5)
    chatgpt_response = []
    if results:
        top_results = results['results'][:3]
        for i, result in enumerate(top_results, 1):
            print(f"Cohere's top result {i}: {result}")

            prompt = ('Resposta em português: Se focando nas respostas do Cohere, dê uma breve explicação '
                      'usando termos mais claros e usando exemplos sobre as habilidades de gema de Path of Exile '
                      'para um jogador novo.\nRetorne neste padrão:\nNome da Gema - Detalhes - Exemplo:')
            chatgpt_prompt = f'{prompt}\n\n{query}\n\n{result}'
            chatgpt_response = get_chatgpt_response(chatgpt_prompt)
            break

    return chatgpt_response
