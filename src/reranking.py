import os
import cohere
import openai
from dotenv import load_dotenv


load_dotenv()


cohere_client = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))
openai.api_key = os.getenv('OPENAI_API_KEY')


def get_chatgpt_response(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  
        prompt=prompt,
        max_tokens=150,  
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

def generate_readable_chatgpt_response(cohere_response):
    response = cohere_response.strip()

    response = response.replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ")

    response = response.replace("o que", "").replace("como", "").replace("que", "").replace("a", "").replace("é", "")

    response = response.replace("Cohere", "").replace("skill gem", "").replace("rerank", "")

    response = response.replace(" ", ", ")

    return response


file_path = 'skill_gem_data/skill_gem_info_treated.txt'
with open(file_path, encoding='utf-8') as file:
    file_content = file.read()


skill_gem_entries = file_content.split('\n')


skill_gem_list = [entry.strip() for entry in skill_gem_entries if entry.strip()]

print('Input your query: ', end='')
query = input()

results = cohere_client.rerank(query=query, documents=skill_gem_list, top_n=5, model='rerank-multilingual-v2.0')


if results:
    top_result = results[0]
    print(f"Cohere's top result: {top_result}")


    chatgpt_prompt = f"Given the query: '{query}', Cohere suggests the skill gem '{top_result}'. What can you tell me about it?"
    chatgpt_response = get_chatgpt_response(chatgpt_prompt)


    print("\nChatGPT Response:")
    print(generate_readable_chatgpt_response(chatgpt_response))
else:
    print("No results from Cohere.")
