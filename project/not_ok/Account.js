module.exports = class Account {
    constructor() {
        this.allowNegBalance = false;
        this.balance = 0;
        this.firstName = '';
    }

    loadFromDB(db, id) {
        var db_acc = db.get_account_by_id(id);
        this.allowNegBalance = db_acc['allow_neg_balance'];
        this.balance = db_acc['balance'];
        this.firstName = db_acc['first_name'];
    }

    Transfer(other, amount) {
        other.addAmount(amount);
        this.balance -= amount * 2;
    }

    addAmount(amount) {
        this.balance += amount
    }
};
