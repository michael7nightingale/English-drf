from rest_framework.test import APITestCase
from django.urls import reverse
from http import HTTPStatus

from services.fixtures import TestAccountFixture


class TestAccountViews(TestAccountFixture, APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    # def test_account_create(self):
    #     account_data = {
    #         "user": {
    #             'username': "ad-aodjlaksmda;lsdasd",
    #             "password": "12asdsdajd",
    #             "email": "sads@gmail.com",
    #         },
    #         "location": "Russia",
    #
    #     }
    #     response = self.client.post(
    #         path=reverse("accounts"),
    #         data=account_data
    #     )
    #     self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_account_detail(self):
        response = self.client1.get(path=reverse("accounts_detail", kwargs={'username': self.account2.user.username}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['email'], self.account2.user.email)

    def test_account_detail_fail_unauthorized(self):
        response = self.client.get(path=reverse("accounts_detail", kwargs={'username': self.account2.user.username}))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_account_detail_not_found(self):
        response = self.client1.get(path=reverse("accounts_detail", kwargs={'username': "self.account2.user.username"}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_account_me(self):
        response = self.client1.get(path=reverse("accounts_me"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['username'], self.account1.user.username)
        self.assertEqual(response.json()['email'], self.account1.user.email)
        self.assertEqual(response.json()['score'], self.account1.score)

    def test_account_me_fail_unauthorized(self):
        response = self.client.get(path=reverse("accounts_me"))
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_account_update(self):
        update_data = {
            "location": "Russia123",
            "user": {
                "first_name": "Firstname123"
            }
        }
        response = self.client1.patch(path=reverse("accounts"), data=update_data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.location, update_data['location'])
        self.assertEqual(self.account1.user.first_name, update_data["user"]['first_name'])
