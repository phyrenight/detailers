import os
import unittest
from app import app, db

TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(BASEDIR, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Disable sending emails during unit testing
    #    mail.init_app(app)
    #    self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
