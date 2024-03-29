from django.test import TestCase


class Hometest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """
        Get / must return status code 200
        """
        self.assertEquals(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        self.assertContains(self.response, 'href="/inscricao/"')