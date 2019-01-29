import unittest
from app import create_app, db
from app.api_1_0 import url, freeurl, runningurl
from flask import url_for
import json

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_(self):
        response = self.client.get(url_for('api.getLongUrls'), data = json.dumps({"url" : "dodia.com/5"}), content_type='application/json')
        self.assertTrue(None in response.get_data(as_text=True))