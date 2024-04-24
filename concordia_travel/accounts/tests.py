from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class AccountsTests(TestCase):

    def setUp(self):
        # Create a test user
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email': 'testuser@example.com'
        }
        User.objects.create_user(**self.credentials)
        # Create the required group
        Group.objects.create(name='normal_users')

    # ... your other test methods ...

    def test_login_with_valid_credentials(self):
        # Send login data
        response = self.client.post(reverse('login'), {
            'username': self.credentials['username'],
            'password': self.credentials['password']
        })
        # Should be redirected to home
        self.assertRedirects(response, reverse('index'))

    def test_login_with_invalid_credentials(self):
        # Send login data with an incorrect password
        response = self.client.post(reverse('login'), {
            'username': self.credentials['username'],
            'password': 'wrong'
        }, follow=True) # follow the redirect
        
        # Check if login failed due to invalid credentials
        self.assertEqual(response.status_code, 200) # Now the response should be the final page after the redirect
        self.assertTrue('Invalid credentials' in response.content.decode())


    def test_register_with_new_user(self):
            # Registration data for a new user
            new_user_data = {
                'first_name': 'Test',
                'last_name': 'User',
                'username': 'testuser2',
                'email': 'testuser2@example.com',
                'password1': 'SecretPassword123',
                'password2': 'SecretPassword123',
            }

            # Send registration data
            response = self.client.post(reverse('register'), new_user_data)
            
            # Check that the response is a redirect to the login page
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('login'))
            
            # Verify that the user was created
            self.assertTrue(User.objects.filter(username='testuser2').exists())

    def test_register_with_existing_username(self):
        # Registration data with an existing username
        existing_user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',  # this username is already taken by setUp user
            'email': 'testuser2@example.com',
            'password1': 'SecretPassword123',
            'password2': 'SecretPassword123',
        }
        
        # Send registration data
        response = self.client.post(reverse('register'), existing_user_data, follow=True) # follow the redirect
        
        # Check the response status code
        self.assertEqual(response.status_code, 200) # After following the redirect, should be the final page
        self.assertTrue('Username taken' in response.content.decode())
