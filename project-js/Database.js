class Database {
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
        time.sleep(0.5);
        this.connected = True;
    }

    disconnect() {
        time.sleep(0.5);
        this.connected = False;
    }

    get_account_by_id(id) {
        if (id === 1)
            return this.account_1
    }
}
