## **Setup**

Recomendado instalar o [Pyenv](https://github.com/pyenv-win/pyenv-win), para gerenciar as versões do python.

Para instalar a versão 3.11.2 necessária para o projeto, caso use pyenv, basta rodar o comando `pyenv install 3.11.2` no terminal, para deixar a pasta do projeto com a versão correta, basta rodar o comando `pyenv local 3.11.2` no terminal.
Usamos também a biblioteca `virtualenv`, que cria um ambiente virtual para o projeto, fazendo com que as dependências não se misturem com o ambiente global do python.
Também temos a biblioteca `pre-commit`, que padroniza os códigos de todos os colaboradores antes de subir seus commits.

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
(.venv) > python -m piptools compile
# Instala as dependências
(.venv) > python -m piptools sync
# Instala o pre-commit (padrões de código)
(.venv) > pre-commit install
```

Tudo junto, para facilitar:

```bash
# Windows CMD e Powershell
> python -m pip install virtualenv & python -m virtualenv .venv & .venv\Scripts\activate & python -m pip install pip-tools & python -m piptools compile & python -m piptools sync & pre-commit install
> python -m pip install virtualenv ; python -m virtualenv .venv ; .venv\Scripts\activate ; python -m pip install pip-tools ; python -m piptools compile ; python -m piptools sync ; pre-commit install
```

---

## **Requirements**

Sempre que for instalar uma nova dependência, é necessário atualizar o requirements.txt, para isso, coloque a nova dependencia no `requirements.in` e então rode o comando abaixo:

```bash
# Ativa o ambiente virtual
> .venv\Scripts\activate
# Gera o requirements.txt
(.venv) > python -m piptools compile
# Instala as dependências
(.venv) > python -m piptools sync
```

Tudo junto, para facilitar:

```bash
# Windows CMD e Powershell
> .venv\Scripts\activate & python -m piptools compile & python -m piptools sync
> .venv\Scripts\activate ; python -m piptools compile ; python -m piptools sync
```

---

## **Preparo para execução dos códigos**

Sempre antes de rodar os códigos, é necessário ativar o ambiente virtual, para isso, basta rodar o comando abaixo:

```bash
# Ativa o ambiente virtual
> .venv\Scripts\activate
```

Depois é só rodar o código normalmente, com python.

```bash
# Roda o código
(.venv) > python skill_gem_scrapper.py
```

---

## **Pre-commit**

Caso queira rodar o pre-commit para checar se o código está seguindo os padrões de código, basta rodar o comando abaixo:

```bash
# Ativa o ambiente virtual
> .venv\Scripts\activate
# Roda o pre-commit
(.venv) > pre-commit run --all-files
```

---

## **Observações**

Para desativar o ambiente virtual, rodar o comando `deactivate`.<br>

```bash
(.venv) >            # Ativo
(.venv) > deactivate # Comando de desativar
>                    # Não ativo
```

Outro ponto importante é verificar se o ambiente virtual está ativo antes de rodar os comandos de requerimento, caso não esteja, ele vai desinstalar/atualizar as dependências do seu ambiente global, o que pode causar problemas.

## **Testes**

Para rodar os testes, basta rodar o comando `pytest` no terminal.
