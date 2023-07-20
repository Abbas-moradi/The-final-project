from django.test import TestCase, Client
from django.urls import reverse
from .models import OtpCode, User
from .forms import UserRegisterationForm, VerifyCodeForm
from django.test import TestCase
from .models import User, Address, OtpCode


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'full_name': 'John Doe',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.phone_number, self.user_data['phone_number'])
        self.assertEqual(self.user.full_name, self.user_data['full_name'])
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)

    def test_str_representation(self):
        expected_str = self.user_data['email']
        self.assertEqual(str(self.user), expected_str)

    def test_has_perm(self):
        self.assertTrue(self.user.has_perm('dummy_perm'))

    def test_has_module_perms(self):
        self.assertTrue(self.user.has_module_perms('dummy_app_label'))


class AddressModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'full_name': 'John Doe',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.address_data = {
            'user': self.user,
            'province': 'Test Province',
            'city': 'Test City',
            'street': 'Test Street',
            'license_plate': 1234,
        }
        self.address = Address.objects.create(**self.address_data)

    def test_create_address(self):
        self.assertEqual(self.address.user, self.user)
        self.assertEqual(self.address.province, self.address_data['province'])
        self.assertEqual(self.address.city, self.address_data['city'])
        self.assertEqual(self.address.street, self.address_data['street'])
        self.assertEqual(self.address.license_plate, self.address_data['license_plate'])

    def test_str_representation(self):
        expected_str = f'{self.user} as {self.address_data["province"]} - {self.address_data["city"]}'
        self.assertEqual(str(self.address), expected_str)


class OtpCodeModelTest(TestCase):
    def setUp(self):
        self.otp_code_data = {
            'phone_number': '1234567890',
            'code': 1234,
        }
        self.otp_code = OtpCode.objects.create(**self.otp_code_data)

    def test_create_otp_code(self):
        self.assertEqual(self.otp_code.phone_number, self.otp_code_data['phone_number'])
        self.assertEqual(self.otp_code.code, self.otp_code_data['code'])

    def test_str_representation(self):
        expected_str = f'{self.otp_code_data["phone_number"]} - {self.otp_code_data["code"]} - {self.otp_code.created}'
        self.assertEqual(str(self.otp_code), expected_str)



class UserRegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:register')

    def test_register_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], UserRegisterationForm)

    def test_register_post(self):
        data = {
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'full_name': 'John Doe',
            'password': 'testpassword',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:verify_code'))

        # Make sure the session data is set correctly
        session_data = self.client.session['user_registration_info']
        self.assertEqual(session_data['phone_number'], data['phone_number'])
        self.assertEqual(session_data['email'], data['email'])
        self.assertEqual(session_data['full_name'], data['full_name'])
        self.assertEqual(session_data['password'], data['password'])

        # Verify that the OtpCode instance is created in the database
        otp_code_instance = OtpCode.objects.get(phone_number=data['phone_number'])
        self.assertIsNotNone(otp_code_instance)

class UserRegisterVerifyCodeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.verify_url = reverse('accounts:verify_code')

        # Prepare session data for user registration
        data = {
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'full_name': 'John Doe',
            'password': 'testpassword',
        }
        self.client.post(self.register_url, data)

    def test_verify_code_get(self):
        response = self.client.get(self.verify_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/verify.html')
        self.assertIsInstance(response.context['form'], VerifyCodeForm)

    def test_verify_code_post_success(self):
        user_session = self.client.session['user_registration_info']
        otp_code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        data = {
            'code': otp_code_instance.code,
        }
        response = self.client.post(self.verify_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))

        # Verify that the user is created in the database
        self.assertTrue(User.objects.filter(phone_number=user_session['phone_number']).exists())
        self.assertEqual(User.objects.get(phone_number=user_session['phone_number']).email, user_session['email'])

        # Verify that the OtpCode instance is deleted from the database
        with self.assertRaises(OtpCode.DoesNotExist):
            OtpCode.objects.get(phone_number=user_session['phone_number'])

    def test_verify_code_post_failure(self):
        data = {
            'code': '000000',  # Invalid code
        }
        response = self.client.post(self.verify_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:verify_code'))

        # Verify that the OtpCode instance still exists in the database
        user_session = self.client.session['user_registration_info']
        self.assertTrue(OtpCode.objects.filter(phone_number=user_session['phone_number']).exists())
