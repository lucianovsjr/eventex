from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class subscribeGet(TestCase):
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
        tags = (('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name="Luciano Vieira", cpf="123456789",
                    email="lucianovsjr@hotmail.com", phone="21 123456789")
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        '''valid POST should redirect to /inscricao/'''
        self.assertEquals(302, self.response.status_code)#302 status de redirecionamento

    def test_send_subscribe_email(self):
        self.assertEquals(1, len(mail.outbox))


class SubscribePostInvalid(TestCase):
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