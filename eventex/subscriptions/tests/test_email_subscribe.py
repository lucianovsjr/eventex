from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name="Luciano Vieira", cpf="123456789",
                    email="lucianovsjr@hotmail.com", phone="21 123456789")
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]#Guarda a lista de emails enviados

    def test_subscribe_email_subject(self):
        expect = 'confirmação de inscrição'

        self.assertEquals(expect, self.email.subject)

    def test_subcribe_email_from(self):
        expect = 'contato@gmail.com'

        self.assertEquals(expect, self.email.from_email)

    def test_subscribe_email_to(self):
        expect = ['contato@gmail.com', 'lucianovsjr@hotmail.com']

        self.assertEquals(expect, self.email.to)

    def test_subscribe_email_body(self):
        contents = ['Luciano Vieira',
                    '123456789',
                    'lucianovsjr@hotmail.com',
                    '21 123456789']

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)