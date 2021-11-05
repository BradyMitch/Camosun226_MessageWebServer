from django.test import TestCase
from msgserver.models import Message
import json

class MessageTestCase (TestCase):
    # PURPOSE:
    # Test creating a key-msg pair
    # Assert that key-msg pair is stored in database
    #
    def test_create_msg(self):
        create = self.client.post("/msgserver/create", {'key':'1234abcd', 'msg':'Test'})
        m = Message.objects.get(key='1234abcd')
        self.assertEqual(m.msg, 'Test')
    
    # PURPOSE:
    # Test getting a msg from a previously set key-msg pair
    # Assert that page returns the key and msg json
    #
    def test_get_msg(self):
        create = self.client.post("/msgserver/create", {'key':'1234abcd', 'msg':'Test'})
        get = self.client.get("/msgserver/get/1234abcd")
        self.assertEqual(get._container[0], b'{"key": "1234abcd", "msg": "Test"}')

    # PURPOSE:
    # Test that duplicate keys cant be made
    # Attempt to create 2 key-msg pairs with the same key
    # Assert for error msg when attempting to create the second pair
    #
    def test_no_duplicate_keys(self):
        create = self.client.post("/msgserver/create", {'key':'1234abcd', 'msg':'Test'})
        create = self.client.post("/msgserver/create", {'key':'1234abcd', 'msg':'TestDup'})
        self.assertIn(b'Message with this Key already exists', create._container[0])

    # PURPOSE:
    # Test updating a msg
    # Create key-msg pair, update key with new msg
    # Assert that msg has changed for given key
    #
    def test_update_msg(self):
        create = self.client.post("/msgserver/create", {'key':'1234abcd', 'msg':'Test'})
        update = self.client.post("/msgserver/update/1234abcd", {'msg':'NewTest'})
        m = Message.objects.get(key='1234abcd')
        self.assertEqual(m.msg, 'NewTest')

    # PURPOSE:
    # Test key constraints
    # 1. Test key size under length 8 
    # (shouldn't save key-msg pair, resulting in a "No message found.")
    # 2. Test key size over length 8 
    # (shouldn't save key-msg pair, resulting in a "No message found.")
    # 3. Test key with non-alphanumeric character "-"
    # (shouldn't save key-msg pair, resulting in a "No message found.")
    # 4. Test key can be alphanumeric (not just numeric)
    # (should work and save key-msg pair)
    #
    def test_key_constraints_enforced(self):
        create = self.client.post("/msgserver/create", {'key':'1234abc', 'msg':'Test'})
        get = self.client.get("/msgserver/get/1234abc")
        self.assertIn(b'No message found.', get._container[0])

        create = self.client.post("/msgserver/create", {'key':'1234abcde', 'msg':'Test'})
        get = self.client.get("/msgserver/get/1234abcde")
        self.assertIn(b'No message found.', get._container[0])

        create = self.client.post("/msgserver/create", {'key':'1234abc-', 'msg':'Test'})
        get = self.client.get("/msgserver/get/1234abc-")
        self.assertIn(b'No message found.', get._container[0])

        create = self.client.post("/msgserver/create", {'key':'1234abcd', 'msg':'Test'})
        m = Message.objects.get(key='1234abcd')
        self.assertEqual(m.msg, 'Test')

    # Purpose:
    # Test msg constraint (max length of 160 characters)
    # Creates key-msg pair w/ msg length of 161 charcters
    # Asserts the msg from get to match with "No message found."
    #
    def test_msg_constraints_enforced(self):
        create = self.client.post("/msgserver/create", {'key':'1234abcd', 'msg':'01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'})
        get = self.client.get("/msgserver/get/1234abcd")
        self.assertIn(b'No message found.', get._container[0])

    # Purpose:
    # Test if output is in json format
    #
    def test_get_msg_in_json_format(self):
        create = self.client.post("/msgserver/create", {'key':'1234abcd', 'msg':'Test'})
        get = self.client.get("/msgserver/")
        m = json.loads(get.content)
        self.assertEqual(str(m), '[\'{"key": "1234abcd", "msg": "Test"}\']')

