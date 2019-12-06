import time


class Database:
    driver = ''
    connected = False

    account_1 = {
        'allow_neg_balance': False,
        'balance': 500,
        'first_name': 'Alice'
    }

    def __init__(self):
        pass

    def connect(self):
        time.sleep(0.5)
        self.connected = True

    def disconnect(self):
        time.sleep(0.5)
        self.connected = False

    def get_account_by_id(self, id):
        if id == 1:
            return self.account_1
