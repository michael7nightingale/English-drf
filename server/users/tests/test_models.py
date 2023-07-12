from django.conf import settings
from rest_framework.test import APITestCase

from services.fixtures import TestAccountFixture
from users.models import Account


class TestAccountData(TestAccountFixture, APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_account_create(self):
        user_data = {
            "username": "Michael123",
            "password": "passwordasd",
            "email": "sdasd@gmail.com",

        }
        account = Account.objects.create_account(
            user=user_data,
            location="Russia"
        )
        self.assertEqual(account.user.email, user_data['email'])
        self.assertEqual(account.user.is_active, False)
        self.assertEqual(account.location, "Russia")
        self.assertFalse(account.avatar)
        self.assertEqual(account.score, 0)
        self.assertEqual(account.level, "A1")

    def test_account_exist_superuser(self):
        self.assertTrue(
            Account.objects.filter(user__username=settings.CHATGPT_USERNAME).exists()
        )

    def test_account_add_score(self):
        score_before = self.account1.score
        self.account1.add_score(10)
        self.assertEqual(self.account1.score - score_before, 10)

    def test_account_add_score_fail(self):
        score_before = self.account1.score
        self.account1.add_score(11)
        self.assertEqual(self.account1.score - score_before, 0)

    def test_account_add_score_level(self):
        score_before = self.account1.score
        level_before = self.account1.level
        for i in range(100):
            self.account1.add_score(10)

        self.assertNotEqual(level_before, self.account1.level)
        self.assertEqual(self.account1.score - score_before, 1000)
