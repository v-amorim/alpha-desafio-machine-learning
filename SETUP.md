## **Setup**

Recomendado instalar o [Pyenv](https://github.com/pyenv-win/pyenv-win), para gerenciar as versões do python.

Para instalar a versão 3.11.2 necessária para o projeto, basta rodar o comando `pyenv install 3.11.2` no terminal.

```bash
# Instala a biblioteca de ambiente virtual
> python -m pip install virtualenv
# Cria o ambiente virtual
> virtualenv .venv
# Ativa o ambiente virtual
> .venv\Scripts\activate
# Instala o pip-tools
(.venv) > python -m pip install pip-tools
# Gera o requirements.txt
(.venv) > pip-compile --upgrade --resolver=backtracking
# Instala as dependências
(.venv) > pip-sync
```

Tudo junto, para facilitar:

```bash
# Windows CMD e Powershell
> python -m pip install virtualenv & virtualenv .venv & .venv\Scripts\activate & python -m pip install pip-tools & pip-compile --upgrade --resolver=backtracking & pip-sync
> python -m pip install virtualenv ; virtualenv .venv ; .venv\Scripts\activate ; python -m pip install pip-tools ; pip-compile --upgrade --resolver=backtracking ; pip-sync
```

---

## **Requirements**

```bash
# Ativa o ambiente virtual
> .venv\Scripts\activate
# Gera o requirements.txt
(.venv) > pip-compile --upgrade --resolver=backtracking
# Instala as dependências
(.venv) > pip-sync
```

Tudo junto, para facilitar:

```bash
# Windows CMD e Powershell
> .venv\Scripts\activate & pip-compile --upgrade --resolver=backtracking & pip-sync
> .venv\Scripts\activate ; pip-compile --upgrade --resolver=backtracking ; pip-sync
```

- Rodando o script `helper.bat` com a opção Atualizar dependencias

---

## **Observações**

Para desativar o ambiente virtual, rodar o comando `deactivate`.<br>

```bash
(.venv) >            # Ativo
(.venv) > deactivate # Comando de desativar
>                    # Não ativo
```

Outro ponto importante é verificar se o ambiente virtual está ativo antes de rodar os comandos de requerimento, caso não esteja, ele vai desinstalar/atualizar as dependências do seu ambiente global, o que pode causar problemas.

## **Verificações pre-commit**

Conseguimos verificar se o código está seguindo os padrões de código com o pre-commit. Ele é um framework que executa scripts antes de cada commit, e se algum deles falhar, o commit não é realizado.<br>
Para instalar o pre-commit, basta rodar o comando `pre-commit install` no terminal (dentro do ambiente virtual).<br>
Para rodar o pre-commit manualmente, basta rodar o comando `pre-commit run --all-files` no terminal.

## **Testes**

Para rodar os testes, basta rodar o comando `pytest` no terminal.

## **Problemas conhecidos**
