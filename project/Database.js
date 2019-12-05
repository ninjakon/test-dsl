function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
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

    async connect() {
        await sleep(500);
        this.connected = true;
    }

    async disconnect() {
        await sleep(500);
        this.connected = false;
    }

    get_account_by_id(id) {
        if (id === 1)
            return this.account_1
    }
};
