import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.registration.models import UserProfile
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

    def test_permission_get(self):
        """Check that unauthorized users can't make request to view"""

        self.client.logout()

        error_message = "Authentication credentials were not provided."

        url = reverse("request_change_email")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message

    def test_permission_post(self):
        """Check that unauthorized users can't make request to post passwords"""

        self.client.logout()

        error_message = "Authentication credentials were not provided."

        data = {
            "password": "testpassword12345",
            "password2": "testpassword123456",
        }

        response = self.post(data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message


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

    def test_permission_get(self):
        """Check that unauthorized users can't make request to view"""

        self.client.logout()

        error_message = "Authentication credentials were not provided."

        token = get_user_token(user_id=User.objects.first().id)

        url = reverse("change_email", None, {token})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message

    def test_permission_post(self):
        """Check that unauthorized users can't make request to post email address"""

        self.client.logout()

        error_message = "Authentication credentials were not provided."

        token = get_user_token(user_id=User.objects.first().id)

        response = self.post({"email": "fdsfsdf@email.com"}, token)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message


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

    def test_permission(self):
        """Check that unauthorized users can't make request to view"""

        self.client.logout()

        error_message = "Authentication credentials were not provided."

        token = get_user_token(user_id=User.objects.first().id)

        url = reverse("confirm_change_email", None, {token})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message


class TestUserProfile(APITestCase):
    """Test class for UserProfile model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        self.user_1 = User.objects.create_user(username="test_user", password="test")
        self.user_2 = User.objects.create_user(username="test_user2", password="test")
        self.client.login(username="test_user", password="test")

    def test_userprofile_list(self):
        """
        Ensure we can retrieve the userprofiles collection
        """

        url = reverse("userprofile-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

        assert response.data["results"][0]["user"] == self.user_1.username
        assert not response.data["results"][0]["is_valid"]

        assert response.data["results"][1]["user"] == self.user_2.username
        assert not response.data["results"][1]["is_valid"]

    def test_userprofile_get(self):
        """
        Ensure we can get a single userprofile by id
        """

        user_profile = UserProfile.objects.first()

        url = reverse("userprofile-detail", None, {user_profile.id})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["user"] == self.user_1.username
        assert not response.data["is_valid"]

    def test_userprofile_update(self):
        """
        Ensure we can update a single userprofile by id
        """

        user_profile = UserProfile.objects.first()

        url = reverse("userprofile-detail", None, {user_profile.id})
        new_data = {"information": "test information about user"}
        response = self.client.put(url, new_data, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["user"] == self.user_1.username
        assert response.data["information"] == new_data["information"]
        assert not response.data["is_valid"]

    def test_permission_list(self):
        """Check that unauthorized users can't make request to view the collection of userprofiles"""

        self.client.logout()

        error_message = "Authentication credentials were not provided."

        url = reverse("userprofile-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message

    def test_permission_detail(self):
        """Check that unauthorized users can't make request to view the detail information about userprofile"""

        self.client.logout()

        error_message = "Authentication credentials were not provided."

        user_profile = UserProfile.objects.first()

        url = reverse("userprofile-detail", None, {user_profile.id})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message

    def test_permission_detail_update(self):
        """Check that unauthorized users can't make request to update the detail information about userprofile"""

        self.client.logout()
        self.client.login(username="testuser2", password="test")

        error_message = "Authentication credentials were not provided."

        user_profile = UserProfile.objects.first()

        url = reverse("userprofile-detail", None, {user_profile.id})
        response = self.client.put(
            url, {"information": "test_information"}, format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message


class TestUser(APITestCase):
    """Test class for User model"""

    def setUp(self):
        """Initialize necessary fields for testing and log in user to make requests"""

        self.user_1 = User.objects.create_user(
            username="test_user", password="test", email="test_email1@gmail.com"
        )
        self.user_2 = User.objects.create_user(
            username="test_user2", password="test", email="test_email2@gmail.com"
        )
        self.client.login(username="test_user", password="test")

    def test_user_list(self):
        """
        Ensure we can retrieve the users collection
        """

        url = reverse("user-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

        assert response.data["results"][0]["id"] == self.user_2.id
        assert response.data["results"][0]["username"] == self.user_2.username
        assert response.data["results"][0]["email"] == self.user_2.email
        assert response.data["results"][0]["profile"]["id"] == self.user_2.profile.id

        assert response.data["results"][1]["id"] == self.user_1.id
        assert response.data["results"][1]["username"] == self.user_1.username
        assert response.data["results"][1]["email"] == self.user_1.email
        assert response.data["results"][1]["profile"]["id"] == self.user_1.profile.id

    def test_user_get(self):
        """
        Ensure we can get a single user by id
        """

        url = reverse("user-detail", None, {self.user_1.id})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["id"] == self.user_1.id
        assert response.data["username"] == self.user_1.username
        assert response.data["email"] == self.user_1.email
        assert response.data["profile"]["id"] == self.user_1.profile.id

    def test_permission_list(self):
        """Check that unauthorized users can't make request to view the collection of users"""

        self.client.logout()

        error_message = "Authentication credentials were not provided."

        url = reverse("user-list")
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message

    def test_permission_detail(self):
        """Check that unauthorized users can't make request to view detail information about user"""

        self.client.logout()

        error_message = "Authentication credentials were not provided."

        url = reverse("user-detail", None, {self.user_1.id})
        response = self.client.get(url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == error_message
