class Account:
    allowNegBalance = False
    balance = 0
    firstName = ''

    def __init__(self):
        pass

    def loadFromDB(self, db, id):
        db_acc = db.get_account_by_id(id)
        self.allowNegBalance = db_acc['allow_neg_balance']
        self.balance = db_acc['balance']
        self.firstName = db_acc['first_name']

    def Transfer(self, other, amount):
        other.addAmount(amount)
        self.balance -= amount * 2

    def addAmount(self, amount):
        self.balance += amount
