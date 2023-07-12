from rest_framework.test import APITestCase, APIClient

from users.models import User, Account


class TestUserFixture(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username="aspodaisoidkja",
            password="asdkaksd",
            email="A9daskdlma@gmail.com",
            first_name="asdasd",
            last_name="ASDsdoaksd"
        )
        cls.user2 = User.objects.create_user(
            username="aspo123daisoidkja",
            password="asaka123ksd",
            email="A9dagsd1skdlma@gmail.com",
            first_name="asdasd",
            last_name="ASDsdoaksd"
        )
        cls.user3 = User.objects.create_user(
            username="aspoadaisoidkja",
            password="asdkagaksd",
            email="A9dasagkdlma@gmail.com",
            first_name="asagdasd",
            last_name="ASDsdoaksd"
        )

        cls.client1 = APIClient()
        cls.client1.force_login(cls.user1)
        cls.client2 = APIClient()
        cls.client2.force_login(cls.user2)
        cls.client3 = APIClient()
        cls.client3.force_login(cls.user3)


class TestAccountFixture(TestUserFixture, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.account1 = Account(
            user=cls.user1,
            location="Russia"
        )
        cls.account1.save()
        cls.account2 = Account(
            user=cls.user2,
            location="Albania"
        )
        cls.account2.save()
        cls.account3 = Account(
            user=cls.user3,
            location="China"
        )
        cls.account3.save()
