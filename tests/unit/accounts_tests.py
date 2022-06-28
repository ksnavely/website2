"""
_accounts_tests_

Unit tests coverage for website.accounts.
"""
import unittest
from unittest import mock

from website import accounts


class AccountTests(unittest.TestCase):
    """
    Test the create/get/update/delete account functionality.
    """

    @mock.patch("website.accounts.MongoClient")
    def client_singleton_test(self, m_mc):
        """
        Make sure we can fetch the mongo client, and that it's a singleton.
        """
        m_mc.return_value = mock.Mock()

        client1 = accounts._client()
        client2 = accounts._client()
        self.assertEqual(client1, client2)

    def bcrypt_test(self):
        """
        Test the account hashing/checking functionality. Verify both the success
        and failure case.
        """
        password = "I love dachsunds#$$@#24!!"
        bad_password = "not my password"

        hashed = accounts._get_hashed_password(password)

        self.assertTrue(accounts._check_password(password, hashed))
        self.assertFalse(accounts._check_password(bad_password, hashed))

    @mock.patch("website.accounts._get_account")
    def authenticate_test(self, m_get_account):
        user = "someuser"
        password = "I love dachsunds#$$@#24!!"
        hashed = accounts._get_hashed_password(password)
        m_get_account.return_value = {"hashed_password": hashed}

        self.assertTrue(accounts.authenticate(user, password))

        m_get_account.assert_called_once_with(user)

    @mock.patch("website.accounts.arrow.utcnow")
    @mock.patch("website.accounts._get_hashed_password")
    @mock.patch("website.accounts._create_account")
    def create_account_test(self, m_c_account, m_get_hashed, m_utc):
        """
        Cover the account creation path.
        """
        ack = "some id"
        m_c_account.return_value = ack

        hashed = "muh hash"
        m_get_hashed.return_value = hashed

        m_for_json_return = 12
        m_utc.return_value.for_json.return_value = m_for_json_return

        username = "some user"
        password = "some pass"

        expected = {
            "_id": username,
            "username": username,
            "hashed_password": hashed,
            "signup_date": m_for_json_return,
        }

        ret = accounts.create_account(username, password)

        self.assertEqual(ack, ret)
        m_c_account.assert_called_once_with(expected)
        m_get_hashed.assert_called_once_with(password)

    @mock.patch("website.accounts._get_auth_collection")
    def get_account_test(self, m_g_auth_collection):
        username = "some user"
        ret = "some mongo cursor"

        ac = mock.Mock()
        ac.find_one = mock.Mock(return_value=ret)
        m_g_auth_collection.return_value = ac

        self.assertEqual(ret, accounts._get_account(username))

        ac.find_one.assert_called_once_with({"_id": username})
