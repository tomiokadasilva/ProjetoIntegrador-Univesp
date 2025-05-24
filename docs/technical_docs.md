# Sistema de Gestão de Clientes i9Robótica - Documentação Técnica

## Arquitetura do Sistema

O Sistema de Gestão de Clientes da i9Robótica é construído utilizando as seguintes tecnologias:

- **Backend**: Flask (framework web Python)
- **Banco de Dados**: MySQL (via ORM SQLAlchemy)
- **Autenticação**: JWT (JSON Web Tokens)
- **Frontend**: HTML, CSS, JavaScript

## Estrutura do Projeto

```
customer_management/
├── venv/                  # Ambiente virtual Python
├── src/                   # Código fonte
│   ├── models/            # Modelos de banco de dados
│   │   ├── user.py        # Modelo de usuário com autenticação
│   │   └── customer.py    # Modelo de cliente com lógica de manutenção
│   ├── routes/            # Endpoints da API
│   │   ├── user.py        # Rotas de usuário e autenticação
│   │   ├── customer.py    # Rotas de gestão de clientes
│   │   └── alert.py       # Rotas de alertas de manutenção
│   ├── static/            # Arquivos estáticos (arquivos frontend)
│   └── main.py            # Ponto de entrada da aplicação
├── scripts/               # Scripts utilitários
│   └── send_maintenance_alerts.py  # Script de notificação por email
├── docs/                  # Documentação
│   ├── user_guide.md      # Documentação para usuário final
│   └── maintenance_alerts.md  # Documentação do sistema de alertas
└── requirements.txt       # Dependências Python
```

## Endpoints da API

### Autenticação

- `POST /api/auth/register` - Registrar novo usuário
- `POST /api/auth/login` - Login de usuário
- `GET /api/auth/profile` - Obter perfil do usuário atual

### Gestão de Usuários

- `GET /api/users` - Listar todos os usuários (apenas admin)
- `GET /api/users/<id>` - Obter detalhes do usuário
- `PUT /api/users/<id>` - Atualizar usuário
- `DELETE /api/users/<id>` - Excluir usuário

### Gestão de Clientes

- `POST /api/customers` - Criar novo cliente
- `GET /api/customers` - Listar todos os clientes
  - Parâmetros de consulta: `name`, `start_date`, `end_date`
- `GET /api/customers/<id>` - Obter detalhes do cliente
- `PUT /api/customers/<id>` - Atualizar cliente
- `DELETE /api/customers/<id>` - Excluir cliente

### Alertas de Manutenção

- `GET /api/alerts` - Obter alertas de manutenção
  - Parâmetros de consulta: `days_threshold`, `start_date`, `end_date`
- `GET /api/alerts/summary` - Obter estatísticas resumidas de alertas

## Esquema do Banco de Dados

### Tabela de Usuários
- `id` (Chave Primária)
- `username` (Único)
- `email` (Único)
- `password_hash`
- `is_admin` (Booleano)
- `created_at`
- `updated_at`

### Tabela de Clientes
- `id` (Chave Primária)
- `name`
- `address`
- `phone`
- `installation_date`
- `created_at`
- `updated_at`

## Sistema de Autenticação

O sistema utiliza JWT (JSON Web Tokens) para autenticação:
1. Usuário faz login com nome de usuário/senha
2. Servidor valida credenciais e emite um token JWT
3. Cliente inclui o token no cabeçalho Authorization para requisições subsequentes
4. Rotas protegidas verificam o token antes de processar as requisições

## Lógica de Alertas de Manutenção

As datas de manutenção são calculadas da seguinte forma:
1. Data base de manutenção = data de instalação + 6 meses
2. Alertas são gerados para manutenções previstas dentro de um limite configurável (padrão: 30 dias)
3. Alertas são categorizados como "Atrasados" ou "Próximos" com base na data atual

## Sistema de Notificação por Email

O script de notificação por email (`scripts/send_maintenance_alerts.py`) fornece:
1. Consulta ao banco de dados para próximas manutenções
2. Geração de email HTML com detalhes do cliente
3. Entrega de email via SMTP
4. Interface de linha de comando para execução manual

## Instruções de Implantação

1. Certifique-se de que Python 3.8+ e MySQL estejam instalados
2. Crie e ative o ambiente virtual
3. Instale as dependências: `pip install -r requirements.txt`
4. Configure a conexão com o banco de dados em `src/main.py`
5. Execute a aplicação: `python src/main.py`
6. Acesse a interface web em http://localhost:5000

## Considerações de Segurança

1. Senhas são criptografadas usando as funções de segurança do Werkzeug
2. Tokens JWT expiram após 24 horas
3. Controle de acesso baseado em funções impede operações não autorizadas
4. Validação de entrada previne ataques comuns de injeção

## Melhorias Futuras

1. Implementar tarefas agendadas automatizadas quando disponíveis
2. Adicionar capacidades de notificação por SMS
3. Desenvolver portal do cliente para autoatendimento
4. Implementar recursos de relatórios e análises
5. Adicionar suporte a múltiplos idiomas
