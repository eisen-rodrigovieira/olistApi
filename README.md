# Integração Sankhya 🔄 Olist

## 📌 Descrição

Este projeto tem como objetivo integrar o sistema de gestão empresarial Sankhya com a API da plataforma Tiny/Olist. A integração visa automatizar a sincronização de informações de cadastro de produtos, movimentação de estoque e pedidos de venda entre os sistemas, permitindo um controle centralizado das operações nos marketplaces disponíveis na Olist.

## 🚀 Tecnologias Utilizadas

- **Python**: Linguagem principal utilizada para desenvolvimento dos scripts de integração.
- **SQL (Oracle PL/SQL)**: Utilizado para manipulação e consulta dos dados no banco de dados Oracle.
- **API Tiny/Olist**: Interface de comunicação com a plataforma Olist para envio e recebimento de dados.
- **Sankhya**: Sistema de gestão empresarial (ERP) utilizado como fonte e destino dos dados integrados.

## 📁 Estrutura do Projeto

A estrutura de diretórios e arquivos do projeto é a seguinte:

```
olistApi/
├── json/                      # Arquivos JSON
│   ├── dml/                   # Valores padrão para interação com o banco de dados Oracle
│   └── objects/               # Estrutura dos objetos para comunicação com API Tiny/Olist
├── keys/                      # Chaves de acesso e credenciais
├── params/                    # Parâmetros e configurações da integração
├── sql/                       # Scripts para criação dos objetos e interação com o banco de dados
├── src/                       # Código-fonte principal do projeto
│   ├── app/                   # Código-fonte da classe aplicação
│   ├── olist/                 # Código-fonte da classe olist
│   ├── sankhya/               # Código-fonte da classe sankhya
│   ├── utils/                 # Código-fonte da classe utils
│   ├── logs/                  # Logs do projeto
│   ├── __init__.py            # Inicializador da interface da aplicação no Streamlit
│   ├── atualiza_estoque.py    # Script para atualização de estoque
│   ├── atualiza_pedidos.py    # Script para atualização de pedidos
│   └── atualiza_produtos.py   # Script para atualização de produtos
├── .gitignore
├── README.md
└── requirements.txt
```

## 🔧 Configuração e Instalação

1. **Clonar o repositório:**

   ```bash
   git clone https://github.com/eisen-rodrigovieira/olistApi.git
   cd olistApi
   ```

2. **Criar e ativar um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instalar as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar os parâmetros de conexão e autenticação:**

   - Criar um arquivo `keys.py` na pasta `keys/` com as informações de acesso à API Tiny/Olist, ao banco de dados Oracle e o sal de criptografia no padrão abaixo.
   ```python
   CLIENT_ID         = 'client_id'
   CLIENT_SECRET     = 'client_secret'
   REDIRECT_URI      = 'redirect_uri'
   FERNET_KEY        = 'fernet_key'
   USERNAME          = 'username'
   PASSWORD          = 'password'
   DATABASE_PASSWORD = 'database_password'
   DATABASE_USERNAME = 'database_username'
   DATABASE_HOST     = 'database_host'
   SENDER_MAIL       = 'sender_mail'
   SENDER_PASSWORD   = 'sender_password'
   ```

## 📧 Contato

- **Email**: [rodrigo.vieira@grupoeisen.com.br](mailto:rodrigo.vieira@grupoeisen.com.br)
- **GitHub**: [dsrodrigovieira](https://github.com/dsrodrigovieira)

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).