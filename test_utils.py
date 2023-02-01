import unittest

from utils import validate_post_body, validate_signup_body, get_password_hash, \
    encode_user_data, decode_user_token, SALT


class PositiveTestCase(unittest.TestCase):

    def test_validate_signup_body(self):
        self.assertEqual(
            validate_signup_body({'email': '1@example.com', 'password': '12345678'}),
            ({'email': '1@example.com', 'password': '12345678'}, None))

    def test_validate_post_body(self):
        self.assertEqual(validate_post_body({"text": "Text 1"}), ({"text": "Text 1"}, None))


class NegativeTestCase(unittest.TestCase):

    def test_validate_signup_body_invalid_email(self):
        self.assertEqual(validate_signup_body({'email': '1example.com', 'password': '12345678'}),
                         (None, 'Invalid email'))
        self.assertEqual(validate_signup_body({'email': '1@examplecom', 'password': '12345678'}),
                         (None, 'Invalid email'))
        self.assertEqual(validate_signup_body({'email': '12345678', 'password': '12345678'}),
                         (None, 'Invalid email'))

    def test_validate_signup_body_email_or_password_are_missing(self):
        self.assertEqual(validate_signup_body({'password': '12345678'}),
                         (None, 'Email or Password fields are missing'))
        self.assertEqual(validate_signup_body({'email': '12345678'}),
                         (None, 'Email or Password fields are missing'))

    def test_validate_signup_body_short_password(self):
        self.assertEqual(validate_signup_body({'email': '1@example.com', 'password': '1234567'}),
                         (None, 'Password should be more than 8 characters'))
        self.assertEqual(validate_signup_body({'email': '1@example.com', 'password': 'qwerty'}),
                         (None, 'Password should be more than 8 characters'))

    def test_validate_post_body_text_missing(self):
        self.assertEqual(validate_post_body({}), (None, 'Text field is missing'))


if __name__ == '__main__':
    unittest.main()
