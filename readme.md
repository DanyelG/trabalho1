# 🔐 Django Auth Project

Aplicação web de autenticação de usuários desenvolvida com **Django** e banco de dados **SQLite**, como parte de atividade acadêmica.

![CI](https://github.com/DanyelG/trabalho1/actions/workflows/django-ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![SQLite](https://img.shields.io/badge/Banco-SQLite-lightgrey)

---

## 📋 Funcionalidades

- Cadastro de usuário com nome, e-mail único e senha
- Senha armazenada com hash seguro (PBKDF2)
- Login com validação de credenciais
- Dashboard protegido por autenticação
- Logout
- Redirecionamento automático para usuários já autenticados

---

## 🗂️ Estrutura do Projeto

```
trabalho1/
└── trabalho0/
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
    └── requirements.txt
```

---

## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.10 ou superior
- pip

### 1. Clone o repositório

```bash
git clone https://github.com/DanyelG/trabalho1.git
cd trabalho1/trabalho0
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
python manage.py makemigrations accounts
python manage.py migrate
```

### 5. (Opcional) Crie um superusuário

```bash
python manage.py createsuperuser
```

---

## ▶️ Executando a Aplicação

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

---

## 🧪 Executando os Testes

```bash
python manage.py test accounts --verbosity=2
```

Os testes utilizam um banco de dados SQLite em memória criado e destruído automaticamente a cada execução — sem necessidade de configuração adicional.

### Cenários cobertos

| # | Cenário | Tipo |
|---|---------|------|
| 1 | Cadastro de usuário com sucesso | Obrigatório |
| 2 | Cadastro com e-mail já existente | Obrigatório |
| 3 | Login com credenciais válidas | Obrigatório |
| 4 | Login com credenciais inválidas | Obrigatório |
| 5 | Senha armazenada com hash (não em texto plano) | Extra |
| 6 | Acesso ao dashboard sem autenticação redireciona | Extra |
| 7 | Acesso ao dashboard autenticado exibe dados do usuário | Extra |
| 8 | Logout encerra a sessão | Extra |
| 9 | Cadastro com senhas diferentes falha | Extra |
| 10 | Usuário já logado é redirecionado ao acessar /login/ | Extra |

---

## 🔁 Integração Contínua (CI)

O projeto utiliza **GitHub Actions** para rodar os testes automaticamente a cada push ou pull request na branch `main`.

O pipeline executa:
1. Instalação do Python 3.12
2. Instalação das dependências
3. Geração e aplicação das migrações
4. Verificação das configurações do projeto
5. Execução dos testes de integração

Arquivo de configuração: `.github/workflows/django-ci.yml`

---

## 🔒 Segurança

- Senhas armazenadas com hash **PBKDF2** (padrão do Django)
- E-mail único por usuário, validado no banco de dados
- Proteção **CSRF** ativa em todos os formulários
- Área restrita protegida por `@login_required`
- Model de usuário customizado com e-mail como campo de autenticação

---

## 🛠️ Tecnologias utilizadas

- [Python 3.12](https://www.python.org/)
- [Django 4.2](https://www.djangoproject.com/)
- [SQLite](https://www.sqlite.org/)
- [GitHub Actions](https://github.com/features/actions)