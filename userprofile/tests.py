from django.test import TestCase, Client
from userprofile.models import UserProfile
import json

class UserProfileAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = '/user-profile/profiles/'
        self.profile = UserProfile.objects.create(name="Test User", email="test@example.com")
        self.detail_url = f'/user-profile/profiles/{self.profile.id}/'

    def test_create_profile_success(self):
        payload = {
            "name": "Alice",
            "email": "alice@example.com"
        }
        response = self.client.post(self.list_url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Profile created successfully")

    def test_create_profile_missing_name(self):
        payload = {
            "email": "bob@example.com"
        }
        response = self.client.post(self.list_url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name is required', response.json()['error'])

    def test_list_profiles(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))
        self.assertGreaterEqual(len(response.json()), 1)

    def test_retrieve_profile_by_id(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], self.profile.name)

    def test_update_profile(self):
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        response = self.client.put(self.detail_url, json.dumps(update_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['name'], "Updated Name")

    def test_update_profile_invalid_email(self):
        update_data = {
            "email": "invalid-email"
        }
        response = self.client.put(self.detail_url, json.dumps(update_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email format", response.json()['error'])

    def test_delete_profile(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.json()['message'])

    def test_get_nonexistent_profile(self):
        response = self.client.get('/user-profile/profiles/999/')
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_profile(self):
        response = self.client.delete('/user-profile/profiles/999/')
        self.assertEqual(response.status_code, 404)
