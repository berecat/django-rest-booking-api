import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.registration.services.tokens import get_user_token


@pytest.mark.usefixtures("user_instance")
class TestSignUp(APITestCase):
    """Tests for SignUp view"""

    def post(self, data):
        """Function make post request to the endpoint"""

        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        return response

    def test_get_request(self):
        """Ensure that returns correct response after GET method"""

        details = "Please write information below"

        url = reverse("signup")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["details"] == details

    def test_right_post_request(self):
        """
        Ensure that returns correct response after POST method
        Since we write correct information view has to return 201 status code
        And correct details message
        """

        details = "You are successfully registered. Please confirm your email address to complete the registration."

        data = {
            "username": "Ivan",
            "email": "soldatenkoivan36@gmail.com",
            "password": "testpassword1234",
            "password2": "testpassword1234",
        }
        response = self.post(data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["details"] == details

    def test_post_request_with_not_matched_password(self):
        """
        Ensure that returns correct response after POST method
        Since we write not matched passwords view has to return 400 status code
        And raise ValidationError for password field
        """

        data = {
            "username": "Ivan",
            "email": "soldatenkoivan36@gmail.com",
            "password": "testpassword1234",
            "password2": "testpassword12344",
        }
        response = self.post(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["password"][0]) == "Password fields didn't match."

    def test_post_request_with_exist_email(self):
        """
        Ensure that returns correct response after POST method
        Since we write existed email address view has to return 400 status code
        And raise ValidationError for email field
        """

        user = User.objects.first()
        data = {
            "username": "Ivan",
            "email": user.email,
            "password": "testpassword1234",
            "password2": "testpassword1234",
        }
        response = self.post(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["email"][0]) == "This field must be unique."


@pytest.mark.usefixtures("user_instance")
class TestActivate(APITestCase):
    """Tests for SignUp view"""

    def test_get_request_with_right_token(self):
        """
        Ensure that returns correct response after GET method
        Since view received right user's token, function has to return 200 status code
        And right details message
        """

        details = "Thank you for your email confirmation."
        token = get_user_token(user_id=User.objects.first().id)

        url = reverse("activate", None, {token})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["details"] == details

    def test_get_request_with_wrong_token(self):
        """
        Ensure that returns correct response after GET method
        Since view received wrong user's token, function has to return 400 status code
        And right details message
        """

        details = "Invalid link!"
        token = get_user_token(user_id=User.objects.first().id)[:-4]

        url = reverse("activate", None, {token})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["details"] == details
