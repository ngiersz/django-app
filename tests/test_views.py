from django.test import TestCase


class TestCalls(TestCase):

    def test_call_view_denies_anonymous(self):
        response = self.client.get('/account/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/account/')

        response = self.client.get('/orders/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/orders/')

        response = self.client.get('/orders/new/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/orders/new/')

        response = self.client.get('/orders_all/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/orders_all/')

        response = self.client.get('/orders_accepted/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/orders_accepted/')
