from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class subscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subcription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name="Luciano Vieira", cpf="123456789",
                    email="lucianovsjr@hotmail.com", phone="21 123456789")
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        '''valid POST should redirect to /inscricao/'''
        self.assertEquals(302, self.response.status_code)#302 status de redirecionamento

    def test_send_subscribe_email(self):
        self.assertEquals(1, len(mail.outbox))

    def test_subscribe_email_subject(self):
        email = mail.outbox[0]#Guarda a lista de emails enviados
        expect = 'confirmação de inscrição'

        self.assertEquals(expect, email.subject)

    def test_subcribe_email_from(self):
        email = mail.outbox[0]  # Guarda a lista de emails enviados
        expect = 'contato@eventex@gamail.com'

        self.assertEquals(expect, email.from_email)

    def test_subscribe_email_to(self):
        email = mail.outbox[0]  # Guarda a lista de emails enviados
        expect = ['contato@gmail.com', 'lucianovsjr@hotmail.com']

        self.assertEquals(expect, email.to)

    def test_subscribe_email_body(self):
        email = mail.outbox[0]  # Guarda a lista de emails enviados

        self.assertIn('Luciano Vieira', email.body)
        self.assertIn('123456789', email.body)
        self.assertIn('lucianovsjr@hotmail.com', email.body)
        self.assertIn('21 123456789', email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEquals(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Luciano Vieira', cpf='123456789',
                    email='lucianovsjr@hotmail.com', phone='21 123456789')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')