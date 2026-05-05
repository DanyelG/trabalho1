# Django Auth Project

Aplicação web com cadastro e autenticação de usuários, desenvolvida com Django e banco de dados SQLite.

## Funcionalidades

- Cadastro de usuário (nome, e-mail único, senha com hash seguro)
- Login com validação de credenciais
- Dashboard protegido por autenticação
- Logout
- Testes de integração cobrindo todos os fluxos principais

## Pré-requisitos

- Python 3.10 ou superior
- pip

## Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/django-auth-project.git
cd django-auth-project
```

### 2. Crie e ative o ambiente virtual

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrações

```bash
python manage.py migrate
```

### 5. (Opcional) Crie um superusuário para acessar o admin

```bash
python manage.py createsuperuser
```

## Executando a Aplicação

```bash
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

| Rota | Descrição |
|------|-----------|
| `/register/` | Cadastro de novo usuário |
| `/login/` | Login |
| `/logout/` | Logout |
| `/dashboard/` | Área restrita (requer login) |
| `/admin/` | Painel administrativo |

## Executando os Testes

```bash
python manage.py test accounts
```

Os testes utilizam um banco de dados SQLite em memória separado, criado e destruído automaticamente a cada execução.

### Cenários testados

| # | Cenário |
|---|---------|
| 1 | Cadastro de usuário com sucesso |
| 2 | Cadastro com e-mail já existente |
| 3 | Login com credenciais válidas |
| 4 | Login com credenciais inválidas |
| 5 | Acesso ao dashboard sem autenticação (redirecionamento) |
| 6 | Acesso ao dashboard autenticado |
| 7 | Logout encerra a sessão |
| 8 | Cadastro com senhas que não coincidem |
| 9 | Cadastro com campos obrigatórios ausentes |
| 10 | Usuário já logado é redirecionado ao acessar /login/ |

## Estrutura do Projeto

```
django_auth_project/
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── django_auth_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   ├── base.html
│   └── accounts/
│       ├── dashboard.html
│       ├── login.html
│       └── register.html
├── manage.py
├── requirements.txt
└── README.md
```

## Segurança

- Senhas armazenadas com hash PBKDF2 (padrão do Django)
- E-mail único por usuário, validado no banco de dados
- Proteção CSRF ativa em todos os formulários
- Área restrita protegida por `@login_required`
- Model de usuário customizado com e-mail como campo de autenticação
