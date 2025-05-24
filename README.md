# i9Robótica - Sistema de Gestão de Clientes e Alertas de Manutenção

## Visão Geral do Projeto

Este projeto é um sistema web desenvolvido para a i9Robótica, uma microempresa especializada na instalação de sistemas repelentes de pombos baseados em campos eletromagnéticos. O sistema visa automatizar o gerenciamento de dados de clientes e o envio de alertas de manutenção preventiva, substituindo processos manuais e melhorando a eficiência operacional.

## Funcionalidades Principais

*   **Gestão de Clientes:** Cadastro, visualização, edição e exclusão de informações de clientes (nome, endereço, telefone, data de instalação).
*   **Filtros e Busca:** Permite filtrar e buscar clientes por nome ou período de instalação.
*   **Alertas de Manutenção:**
    *   Cálculo automático da data de manutenção preventiva (6 meses após a instalação por padrão).
    *   Painel de alertas exibindo manutenções próximas ou vencidas.
    *   Filtro de alertas por período (7, 14, 21, 30, 60, 90 dias).
    *   Definição de período de alerta personalizado por cliente no momento do cadastro/edição.
    *   Notificações visuais (ícone de sino) para alertas críticos (vencidos ou a vencer em 2 dias).
*   **Autenticação de Usuários:** Sistema de login seguro para funcionários.
*   **Gestão de Usuários:** Administradores podem criar, editar e excluir contas de usuários.
*   **Script de Notificação por Email:** Um script (localizado em `scripts/send_maintenance_alerts.py`) pode ser configurado para verificar e enviar emails de alerta para a equipe (requer configuração de servidor SMTP).

## Tecnologias Utilizadas

*   **Backend:** Python, Flask, Flask-SQLAlchemy
*   **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
*   **Banco de Dados:** MySQL
*   **Servidor WSGI:** Gunicorn (para produção via Docker)
*   **Containerização:** Docker, Docker Compose

## Pré-requisitos

*   Docker instalado: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
*   Docker Compose instalado (geralmente incluído com Docker Desktop): [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Instalação e Provisionamento (Usando Docker Compose)

1.  **Clone ou Baixe o Repositório:** Obtenha os arquivos do projeto (se recebeu um zip, extraia-o).
2.  **Navegue até o Diretório do Projeto:** Abra um terminal ou prompt de comando e acesse o diretório raiz do projeto (o diretório que contém `docker-compose.yml` e `Dockerfile`).

    ```bash
    cd caminho/para/customer_management
    ```

3.  **Revise as Variáveis de Ambiente (Opcional mas Recomendado):**
    *   Abra o arquivo `docker-compose.yml`.
    *   **É altamente recomendado alterar os valores padrão** para `MYSQL_ROOT_PASSWORD`, `DB_PASSWORD` e `SECRET_KEY` por questões de segurança.
    *   Se planeja usar o envio de emails, configure as variáveis de ambiente relacionadas ao SMTP ( `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `DEFAULT_SENDER`) no `docker-compose.yml` na seção `environment` do serviço `app`.

4.  **Construa as Imagens e Inicie os Containers:**
    Execute o seguinte comando no terminal:

    ```bash
    docker-compose up --build -d
    ```

    *   `--build`: Constrói as imagens Docker (necessário na primeira vez ou após alterações no código/Dockerfile).
    *   `-d`: Executa os containers em segundo plano (modo detached).
    *   O Docker Compose irá baixar a imagem do MySQL, construir a imagem da aplicação Flask, criar uma rede para eles se comunicarem e iniciar ambos os containers.
    *   Aguarde um momento para que o banco de dados seja inicializado.

5.  **Acesse a Aplicação:**
    Abra seu navegador e acesse: `http://localhost:5000`
    (Se estiver rodando em um servidor remoto, substitua `localhost` pelo IP ou domínio do servidor).

6.  **Primeiro Login (Administrador):**
    *   O sistema não possui um usuário padrão.
    *   O **primeiro usuário a se registrar** através da API (ou se a funcionalidade de registro for reativada na interface) será automaticamente definido como **administrador**.
    *   Atualmente, o registro pela interface está desativado. Novos usuários devem ser criados pelo administrador logado, na seção "Usuários". Para criar o primeiro admin, você pode:
        *   Temporariamente reativar o registro na interface (não recomendado para produção).
        *   Usar uma ferramenta de API (como Postman ou curl) para fazer uma requisição POST para `/api/auth/register` com os dados do primeiro usuário (definindo `is_admin: true` no corpo JSON).
        *   Conectar-se diretamente ao banco de dados Docker e inserir o primeiro usuário na tabela `user`.

## Executando o Script de Alerta por Email

O script `scripts/send_maintenance_alerts.py` verifica os clientes com manutenção próxima e envia emails.

1.  **Configure as Variáveis de Ambiente SMTP:** Certifique-se de que as variáveis de ambiente SMTP (`SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `DEFAULT_SENDER`) estão definidas no ambiente onde o script será executado (ou diretamente no `docker-compose.yml` se for executar dentro do container).
2.  **Execute o Script:**
    *   **Dentro do Container da Aplicação (Recomendado):**
        ```bash
        docker-compose exec app python scripts/send_maintenance_alerts.py
        ```
    *   **Manualmente (se tiver Python e dependências instaladas localmente):**
        ```bash
        # Exporte as variáveis de ambiente necessárias (DB_*, SMTP_*)
        export DB_HOST=localhost # ou o IP/hostname do container DB
        export DB_PORT=3306 # Se exposto
        # ... outras variáveis ...
        python scripts/send_maintenance_alerts.py
        ```

## Parando a Aplicação

Para parar os containers Docker, execute no terminal, no diretório do projeto:

```bash
docker-compose down
```

Isso irá parar e remover os containers, mas os dados do banco de dados persistirão no volume `db_data` (a menos que você remova o volume manualmente com `docker-compose down -v`).

## Estrutura do Projeto

```
/customer_management
|-- Dockerfile             # Define a imagem Docker para a aplicação Flask
|-- docker-compose.yml     # Orquestra os containers da app e do DB
|-- .dockerignore          # Arquivos a serem ignorados pelo Docker build
|-- requirements.txt       # Dependências Python
|-- README.md              # Este arquivo
|-- /src                   # Código fonte da aplicação Flask
|   |-- __init__.py
|   |-- main.py            # Ponto de entrada da aplicação Flask
|   |-- config.py          # Configurações (lê variáveis de ambiente)
|   |-- /models            # Modelos SQLAlchemy (User, Customer)
|   |-- /routes            # Rotas/Blueprints da API Flask
|   |-- /static            # Arquivos estáticos (HTML, CSS, JS do frontend)
|       |-- index.html
|-- /scripts               # Scripts auxiliares
|   |-- send_maintenance_alerts.py
|-- /docs                  # Documentação do projeto
|   |-- maintenance_alerts.md
|   |-- technical_docs.md
|   |-- user_guide.md
```

