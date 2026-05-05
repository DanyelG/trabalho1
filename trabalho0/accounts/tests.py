"""
Testes de Integração - Sistema de Autenticação
==============================================
Cobre os seguintes cenários obrigatórios:
  1. Cadastro de usuário com sucesso
  2. Tentativa de cadastro com e-mail já existente
  3. Login com credenciais válidas
  4. Login com credenciais inválidas

Cenários adicionais:
  5. Acesso ao dashboard sem autenticação (redirecionamento)
  6. Acesso ao dashboard autenticado
  7. Logout
  8. Cadastro com senhas que não coincidem
  9. Cadastro com campos obrigatórios ausentes
  10. Redirecionamento de usuário já logado
"""

from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User


class CadastroUsuarioTest(TestCase):
    """Testes de integração para o fluxo de cadastro de usuário."""

    def setUp(self):
        self.client = Client()
        self.url_cadastro = reverse('register')
        self.dados_validos = {
            'name': 'João Silva',
            'email': 'joao@example.com',
            'password': 'Senha@1234',
            'password_confirm': 'Senha@1234',
        }

    # -------------------------------------------------------
    # Cenário 1: Cadastro com sucesso
    # -------------------------------------------------------
    def test_cadastro_com_sucesso(self):
        """Usuário é cadastrado e redirecionado ao dashboard."""
        response = self.client.post(self.url_cadastro, self.dados_validos)

        # Deve redirecionar para o dashboard após cadastro
        self.assertRedirects(response, reverse('dashboard'))

        # Usuário deve existir no banco de dados
        self.assertTrue(User.objects.filter(email='joao@example.com').exists())

    def test_senha_armazenada_com_hash(self):
        """A senha não deve ser armazenada em texto plano."""
        self.client.post(self.url_cadastro, self.dados_validos)
        user = User.objects.get(email='joao@example.com')

        # A senha armazenada não deve ser igual à senha em texto plano
        self.assertNotEqual(user.password, 'Senha@1234')
        # Deve iniciar com o identificador de hash do Django
        self.assertTrue(user.password.startswith('pbkdf2_') or user.password.startswith('bcrypt'))

    def test_cadastro_cria_sessao_autenticada(self):
        """Após cadastro, o usuário deve estar logado."""
        self.client.post(self.url_cadastro, self.dados_validos)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_pagina_cadastro_acessivel(self):
        """A página de cadastro deve retornar 200."""
        response = self.client.get(self.url_cadastro)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    # -------------------------------------------------------
    # Cenário 2: Cadastro com e-mail já existente
    # -------------------------------------------------------
    def test_cadastro_email_duplicado(self):
        """Não deve permitir cadastro com e-mail já existente."""
        # Primeiro cadastro
        self.client.post(self.url_cadastro, self.dados_validos)
        self.client.logout()

        # Segundo cadastro com o mesmo e-mail
        dados_duplicados = self.dados_validos.copy()
        dados_duplicados['name'] = 'Outro Nome'
        response = self.client.post(self.url_cadastro, dados_duplicados)

        # Não deve redirecionar — deve exibir erro no formulário
        self.assertEqual(response.status_code, 200)

        # Mensagem de erro deve estar na resposta
        self.assertContains(response, 'já está cadastrado')

        # Apenas um usuário deve existir no banco
        self.assertEqual(User.objects.filter(email='joao@example.com').count(), 1)

    # -------------------------------------------------------
    # Cenário extra: Campos inválidos no cadastro
    # -------------------------------------------------------
    def test_cadastro_senhas_diferentes(self):
        """Não deve cadastrar quando as senhas não coincidem."""
        dados = self.dados_validos.copy()
        dados['password_confirm'] = 'SenhaDiferente@999'
        response = self.client.post(self.url_cadastro, dados)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='joao@example.com').exists())

    def test_cadastro_sem_nome(self):
        """Não deve cadastrar sem informar o nome."""
        dados = self.dados_validos.copy()
        dados['name'] = ''
        response = self.client.post(self.url_cadastro, dados)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='joao@example.com').exists())

    def test_cadastro_email_invalido(self):
        """Não deve cadastrar com e-mail em formato inválido."""
        dados = self.dados_validos.copy()
        dados['email'] = 'email-invalido'
        response = self.client.post(self.url_cadastro, dados)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='email-invalido').exists())


class LoginUsuarioTest(TestCase):
    """Testes de integração para o fluxo de login."""

    def setUp(self):
        self.client = Client()
        self.url_login = reverse('login')

        # Cria um usuário para os testes de login
        self.usuario = User.objects.create_user(
            email='maria@example.com',
            name='Maria Souza',
            password='Senha@5678',
        )

    # -------------------------------------------------------
    # Cenário 3: Login com credenciais válidas
    # -------------------------------------------------------
    def test_login_credenciais_validas(self):
        """Login com credenciais corretas deve redirecionar ao dashboard."""
        response = self.client.post(self.url_login, {
            'username': 'maria@example.com',
            'password': 'Senha@5678',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_cria_sessao(self):
        """Após login, o usuário deve conseguir acessar o dashboard."""
        self.client.post(self.url_login, {
            'username': 'maria@example.com',
            'password': 'Senha@5678',
        })
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Souza')

    def test_pagina_login_acessivel(self):
        """A página de login deve retornar 200."""
        response = self.client.get(self.url_login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    # -------------------------------------------------------
    # Cenário 4: Login com credenciais inválidas
    # -------------------------------------------------------
    def test_login_senha_errada(self):
        """Login com senha incorreta deve falhar e exibir erro."""
        response = self.client.post(self.url_login, {
            'username': 'maria@example.com',
            'password': 'SenhaErrada@000',
        })
        # Não deve redirecionar
        self.assertEqual(response.status_code, 200)

    def test_login_email_inexistente(self):
        """Login com e-mail não cadastrado deve falhar."""
        response = self.client.post(self.url_login, {
            'username': 'naoexiste@example.com',
            'password': 'Qualquer@123',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_invalido_nao_cria_sessao(self):
        """Após login inválido, o dashboard deve ser inacessível."""
        self.client.post(self.url_login, {
            'username': 'maria@example.com',
            'password': 'SenhaErrada',
        })
        response = self.client.get(reverse('dashboard'))
        # Deve redirecionar para o login
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_login_campos_vazios(self):
        """Login sem preencher campos deve falhar."""
        response = self.client.post(self.url_login, {
            'username': '',
            'password': '',
        })
        self.assertEqual(response.status_code, 200)


class DashboardAutenticacaoTest(TestCase):
    """Testes de controle de acesso ao dashboard."""

    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(
            email='ana@example.com',
            name='Ana Lima',
            password='Senha@9999',
        )

    # -------------------------------------------------------
    # Cenário extra: Acesso sem autenticação
    # -------------------------------------------------------
    def test_dashboard_sem_autenticacao_redireciona(self):
        """Usuário não autenticado deve ser redirecionado ao login."""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}"
        )

    def test_dashboard_com_autenticacao(self):
        """Usuário autenticado deve acessar o dashboard normalmente."""
        self.client.login(username='ana@example.com', password='Senha@9999')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana Lima')

    # -------------------------------------------------------
    # Cenário extra: Logout
    # -------------------------------------------------------
    def test_logout_encerra_sessao(self):
        """Após logout, o dashboard deve ser inacessível."""
        self.client.login(username='ana@example.com', password='Senha@9999')

        # Confirma que estava logado
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

        # Faz logout
        self.client.get(reverse('logout'))

        # Dashboard deve redirecionar para login
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_usuario_ja_logado_redirecionado_do_login(self):
        """Usuário autenticado acessando /login/ deve ser redirecionado ao dashboard."""
        self.client.login(username='ana@example.com', password='Senha@9999')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('dashboard'))
