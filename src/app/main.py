from __future__ import annotations

from app.reranking import rerank
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='../src/app/templates')
app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.post('/receive-input')
async def receive_input(request: Request):
    try:
        data = await request.json()
        query = data.get('query')
        if not query:
            raise HTTPException(status_code=400, detail='Query não fornecida')

        reranked_results = rerank(query)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao processar a entrada do usuário: {str(e)}') from e

    if reranked_results:
        return JSONResponse(content={'message': 'Input recebido com sucesso!', 'reranked_results': reranked_results})


@app.get('/', response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse('chat_page.html', {'request': request})
