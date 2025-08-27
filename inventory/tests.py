from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Category, InventoryItem

# Create your tests here.
class AuthTests(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_get_token(self):
        response = self.client.post("/api/token/", {
            "username": self.username,
            "password": self.password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_access_protected_without_token(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_with_token(self):
        token_response = self.client.post("/api/token/", {
            "username": self.username,
            "password": self.password
        })
        access_token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryItemTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass1234")
        token_response = self.client.post("/api/token/", {
            "username": "user1",
            "password": "pass1234"
        })
        self.access_token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_category(self):
        response = self.client.post("/api/categories/", {"name": "Electronics"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_create_item(self):
        category = Category.objects.create(name="Books")
        response = self.client.post("/api/items/", {
            "name": "Django Guide",
            "description": "Learn Django",
            "unit_price": "29.99",
            "quantity": 10,
            "category": category.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 1)
        item = InventoryItem.objects.first()
        self.assertEqual(item.name, "Django Guide")
        self.assertEqual(item.unit_price, Decimal("29.99"))

