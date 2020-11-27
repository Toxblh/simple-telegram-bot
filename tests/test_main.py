# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from main import add_new_user, get_user_by_user_id, is_user_exist, reset_users, users, remove_user_by_user_id


class TestSimple(unittest.TestCase):

    def test_reset_users(self):
        users.clear()
        test_user = {
            'user_name': 'first_name',
            'user_id': 123,
            'message_id': 1
        }
        add_new_user(test_user)

        self.assertEqual(test_user, users[0])

        reset_users()

        self.assertEqual(users, [])

    def test_add_user(self):
        reset_users()
        test_user = {
            'user_name': 'first_name',
            'user_id': 'id',
            'message_id': 1
        }
        add_new_user(test_user)

        self.assertEqual(test_user, users[0])

    def test_add_user_three_times(self):
        reset_users()
        test_user = {
            'user_name': 'first_name',
            'user_id': 'id',
            'message_id': 1
        }
        add_new_user(test_user)
        add_new_user(test_user)
        add_new_user(test_user)

        self.assertEqual(test_user, users[2])

    def test_remove_user_by_user_id(self):
        reset_users()
        test_user1 = {
            'user_name': 'first_name',
            'user_id': 123,
            'message_id': 1
        }
        test_user2 = {
            'user_name': 'second_name',
            'user_id': 321,
            'message_id': 2
        }

        add_new_user(test_user1)
        add_new_user(test_user2)

        self.assertEqual(len(users), 2)

        remove_user_by_user_id(test_user1['user_id'])

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], test_user2)

    def test_check_user_await_reply(self):
        reset_users()
        test_user1 = {
            'user_name': 'first_name',
            'user_id': 123,
            'message_id': 1
        }
        test_user2 = {
            'user_name': 'second_name',
            'user_id': 321,
            'message_id': 2
        }

        add_new_user(test_user1)
        add_new_user(test_user2)

        self.assertEqual(is_user_exist(321), True)
        self.assertEqual(is_user_exist(432), False)

    def test_get_user_by_user_id(self):
        reset_users()
        test_user1 = {
            'user_name': 'first_name',
            'user_id': 123,
            'message_id': 1
        }
        test_user2 = {
            'user_name': 'second_name',
            'user_id': 321,
            'message_id': 2
        }

        add_new_user(test_user1)
        add_new_user(test_user2)

        self.assertEqual(get_user_by_user_id(321), test_user2)
        self.assertEqual(get_user_by_user_id(123), test_user1)
        self.assertEqual(get_user_by_user_id(432), False)

        user = get_user_by_user_id(321)

        self.assertEqual(user.get('user_id'), test_user2.get('user_id'))
        self.assertEqual(user.get('user_name'), test_user2.get('user_name'))
        self.assertEqual(user.get('message_id'), test_user2.get('message_id'))


if __name__ == '__main__':
    unittest.main()
