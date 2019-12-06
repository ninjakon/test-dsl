function sleep(ms) {
    var start = new Date().getTime(), expire = start + ms;
    while (new Date().getTime() < expire) { }
}

module.exports = class Database {
    constructor() {
        this.driver = '';
        this.connected = false;
        this.account_1 = {
            'allow_neg_balance': false,
            'balance': 500,
            'first_name': 'Alice'
        }
    }

    connect() {
        sleep(500);
        this.connected = false;
    }

    disconnect() {
        sleep(500);
        this.connected = false;
    }

    get_account_by_id(id) {
        if (id === 1)
            return this.account_1
    }
};
