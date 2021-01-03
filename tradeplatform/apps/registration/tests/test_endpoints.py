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

        error_message = "Password fields didn't match."

        data = {
            "username": "Ivan",
            "email": "soldatenkoivan36@gmail.com",
            "password": "testpassword1234",
            "password2": "testpassword12344",
        }
        response = self.post(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["password"][0]) == error_message

    def test_post_request_with_exist_email(self):
        """
        Ensure that returns correct response after POST method
        Since we write existed email address view has to return 400 status code
        And raise ValidationError for email field
        """

        error_message = "This field must be unique."

        user = User.objects.first()
        data = {
            "username": "Ivan",
            "email": user.email,
            "password": "testpassword1234",
            "password2": "testpassword1234",
        }
        response = self.post(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["email"][0]) == error_message


@pytest.mark.usefixtures("user_instance")
class TestActivate(APITestCase):
    """Tests for Activate view"""

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


@pytest.mark.usefixtures("user_instance")
class TestRequestResetPassword(APITestCase):
    """Tests for RequestResetPassword view"""

    def post(self, data):
        """Function make POST request to tested view"""

        url = reverse("reset")
        response = self.client.post(url, data, format="json")
        return response

    def test_get_request(self):
        """Ensure that view returns correct response after GET method"""

        details = "Please write your email address to reset password."

        url = reverse("reset")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["details"] == details

    def test_wrong_post_request(self):
        """
        Ensure that returns correct response after POST method
        Since view received user's email, which doesn't exist function has to return
        400 status code and right validation error
        """

        error_message = "User with the given email address does not exist."

        response = self.post({"email": "sdfsfsfs@email.com"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["email"][0]) == error_message

    def test_right_post_request(self):
        """
        Ensure that returns correct response after POST method
        Since view received user's email, which exist function has to return
        201 status code and right details information
        """

        details = "We send you confirmation mail for reset your password."

        user = User.objects.first()
        response = self.post({"email": user.email})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["details"] == details


@pytest.mark.usefixtures("user_instance")
class TestResetPassword(APITestCase):
    """Tests for ResetPassword view"""

    def post(self, data, token):
        """Function make POST request to tested view"""

        url = reverse("confirm_reset", None, {token})
        response = self.client.post(url, data, format="json")
        return response

    def test_get_request_with_right_token(self):
        """
        Ensure that returns correct response after GET method
        Since view received right user's token, function has to return 200 status code
        And right details message
        """

        details = "Please write new password and confirm it."
        token = get_user_token(user_id=User.objects.first().id)

        url = reverse("confirm_reset", None, {token})
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

        url = reverse("confirm_reset", None, {token})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["details"] == details

    def test_wrong_post_request(self):
        """
        Ensure that returns correct response after POST method
        Since view received passwords, which didn't matched, function has to return
        400 status code and right validation error
        """

        error_message = "Password fields didn't match."

        data = {
            "password": "testpassword12345",
            "password2": "testpassword123456",
        }
        token = get_user_token(user_id=User.objects.first().id)

        response = self.post(data, token)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["password"][0]) == error_message

    def test_post_request_with_wrong_token(self):
        """
        Ensure that returns correct response after POST method
        Since view received wrong user's token, function has to return 400 status code
        And right details message
        """

        details = "Invalid link!"
        data = {
            "password": "testpassword12345",
            "password2": "testpassword12345",
        }
        token = get_user_token(user_id=User.objects.first().id)[:-4]

        response = self.post(data, token)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["details"] == details

    def test_right_post_request(self):
        """
        Ensure that returns correct response after POST method
        Since view received passwords, which are matched, function has to return
        201 status code and right details information
        """

        details = "Password has been successfully changed."
        data = {
            "password": "testpassword12345",
            "password2": "testpassword12345",
        }
        token = get_user_token(user_id=User.objects.first().id)

        response = self.post(data, token)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["details"] == details


class TestRequestChangeEmailAddress(APITestCase):
    """Test for RequestChangeEmailAddress view"""

    def setUp(self):
        """Initialize variables for testing"""

        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testpassword12345",
        )
        self.client.login(username="testuser", password="testpassword12345")

    def post(self, data):
        """Function make POST request to tested view"""

        url = reverse("request_change_email")
        response = self.client.post(url, data, format="json")
        return response

    def test_get_request(self):
        """Ensure that returns correct response after GET request"""

        details = (
            "You need to write password and confirm it "
            "to change your account email address"
        )

        url = reverse("request_change_email")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["details"] == details

    def test_right_post_request(self):
        """
        Ensure that returns correct response after POST method
        Since view received passwords, which are matched, function has to return
        201 status code and right details information
        """

        details = "We send you confirmation mail for change your email address."
        data = {
            "password": "testpassword12345",
            "password2": "testpassword12345",
        }

        response = self.post(data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["details"] == details

    def test_post_request_with_wrong_password(self):
        """
        Ensure that returns correct response after POST method
        Since view received passwords, which didn't matched with current user's password,
        function has to return 400 status code and right validation error
        """

        error_message = "You write wrong password!"

        data = {
            "password": "testpassword123456",
            "password2": "testpassword123456",
        }

        response = self.post(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["password"][0]) == error_message

    def test_wrong_post_request(self):
        """
        Ensure that returns correct response after POST method
        Since view received passwords, which didn't matched, function has to return
        400 status code and right validation error
        """

        error_message = "Password fields didn't match."

        data = {
            "password": "testpassword12345",
            "password2": "testpassword123456",
        }

        response = self.post(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["password"][0]) == error_message


class TestChangeEmailAddress(APITestCase):
    """Test for ChangeEmailAddress view"""

    def setUp(self):
        """Initialize variables for testing"""

        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testpassword12345",
        )
        self.client.login(username="testuser", password="testpassword12345")

    def post(self, data, token):
        """Function make POST request to tested view"""

        url = reverse("change_email", None, {token})
        response = self.client.post(url, data, format="json")
        return response

    def test_get_request_with_right_token(self):
        """
        Ensure that returns correct response after GET method
        Since view received right user's token, function has to return 200 status code
        And right details message
        """

        details = "Write new email address below."
        token = get_user_token(user_id=User.objects.first().id)

        url = reverse("change_email", None, {token})
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

        url = reverse("change_email", None, {token})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["details"] == details

    def test_wrong_post_request(self):
        """
        Ensure that returns correct response after POST method
        Since view received email, which has already existed, function has to return
        400 status code and right validation error
        """

        error_message = "User with the given email address has already existed"

        token = get_user_token(user_id=User.objects.first().id)

        response = self.post({"email": self.user.email}, token)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["email"][0]) == error_message

    def test_post_request_with_wrong_token(self):
        """
        Ensure that returns correct response after POST method
        Since view received wrong user's token, function has to return 400 status code
        And right details message
        """

        details = "Invalid link!"

        token = get_user_token(user_id=User.objects.first().id)[:-4]

        response = self.post({"email": "fdsfsdf@email.com"}, token)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["details"] == details

    def test_right_post_request(self):
        """
        Ensure that returns correct response after POST method
        Since view received email, which hasn't already existed, function has to return
        201 status code and right details information
        """

        details = "We send you confirmation mail for change your email address."

        token = get_user_token(user_id=User.objects.first().id)

        response = self.post({"email": "fdsfsdf@email.com"}, token)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["details"] == details


class TestActivateChangeEmail(APITestCase):
    """Tests for ActivateChangeEmail view"""

    def setUp(self):
        """Initialize variables for testing"""

        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testpassword12345",
        )
        self.client.login(username="testuser", password="testpassword12345")

    def test_get_request_with_right_token(self):
        """
        Ensure that returns correct response after GET method
        Since view received right user's token, function has to return 200 status code
        And right details message
        """

        details = "Thank for your new email address confirmation."
        token = get_user_token(user_id=User.objects.first().id)

        url = reverse("confirm_change_email", None, {token})
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

        url = reverse("confirm_change_email", None, {token})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["details"] == details
