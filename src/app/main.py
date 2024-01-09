from __future__ import annotations

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from reranking import rerank

app = FastAPI()
templates = Jinja2Templates(directory='src/app/templates')
app.mount('/static', StaticFiles(directory='src/app/static'), name='static')


@app.post('/recive-input')
async def receive_input(request: Request):
    try:
        data = await request.json()
        user_input = data.get('userInput')
        if not user_input:
            raise HTTPException(status_code=400, detail='Input do usuário não fornecido')

        print(f'Received user input: {user_input}')

        resposta_gerada = rerank(user_input)

    except Exception as e:
        print(f'Erro ao processar a entrada do usuário: {str(e)}')
        raise HTTPException(status_code=500, detail=f'Erro ao processar a entrada do usuário: {str(e)}') from e

    if resposta_gerada:
        return JSONResponse(content={'message': 'Input recebido com sucesso!', 'resposta': resposta_gerada})


@app.get('/', response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse('chat_page.html', {'request': request})
