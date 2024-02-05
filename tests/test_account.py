"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db, app
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_repr(self):
        """ Test the representation of an account """
        account = Account()
        account.name = "Foo"
        self.assertEqual(str(account), "<Account 'Foo'>")

    def test_to_dict(self):
        """ Test account to dict """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(account.name, result["name"])
        self.assertEqual(account.email, result["email"])
        self.assertEqual(account.phone_number, result["phone_number"])
        self.assertEqual(account.disabled, result["disabled"])
        self.assertEqual(account.date_joined, result["date_joined"])

    def test_from_dict(self):
        """ Test the attribute from dict """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        accountDict = account.to_dict()
        newAcc = Account()
        newAcc.from_dict(accountDict)
        self.assertEqual(account.name, newAcc.name)
        self.assertEqual(account.email, newAcc.email)
        self.assertEqual(account.phone_number, newAcc.phone_number)
        self.assertEqual(account.disabled, newAcc.disabled)
        self.assertEqual(account.date_joined, newAcc.date_joined)

    def test_account_update(self):
        """ Test Account update in database"""
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()
        #print(account.id)
        # update name and phone num 
        account.name = "Michelle"
        account.email = "mcgowm1@unlv.nevada.edu"
        account.update()
        updateAcc = Account.find(account.id)
        self.assertEqual(updateAcc.name, "Michelle")
        self.assertEqual(updateAcc.email, "mcgowm1@unlv.nevada.edu")
        empty_id = Account()
        try:
            empty_id.update()
        except DataValidationError as e:
            errorMsg = e
        self.assertEqual(str(errorMsg), 'Update called with empty ID field')
        
    
    def test_account_deletion(self):
        """ Test Account deletion in database"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    

