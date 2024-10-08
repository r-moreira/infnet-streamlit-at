# INFNET 
## AT - Frontend com Streamlit
### Aluno: Rodrigo Moreira Avila


### Avisos ao professor:
Eu preferi criar meu próprio sistema de páginas ao invés de usar o nativo do streamlit, que utiliza o diretório pages.

* [Link para acessar o APP](https://infnet-app-at-bdh9wnirzxuufxcrich8sf.streamlit.app/)
* [Link do repositório no GitHub](https://github.com/r-moreira/infnet-streamlit-at)

### Sobre o projeto:
Aplicação para resolver uma série de exercícios com o framework ```Streamlit```


### Estrutura do projeto:
```./README.md``` - Este arquivo.

```./notebook/*``` - Contém o notebook utilizado análise exploratória dos dados.

```./src/*``` - Contém o código fonte da aplicação.

```./data/*``` - Contém os arquivos com os dados.

```./requirements.txt``` - Contém as dependências do projeto.


### Como rodar o projeto streamlit:
1. Configurando versão do python:
```bash
pyenv local 3.11.9
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
```

3. Ative o ambiente virtual:
```bash
source .venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute a aplicação:
```bash
streamlit run src/app.py
```

### Como rodar o notebook:

1. Execute o Jupyter Notebook:
```bash
jupyter notebook
```
