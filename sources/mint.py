import mintapi


def get_balance(email, password, account_id):
    accounts = mintapi.get_accounts(email, password)
    for account in accounts:
        if account['accountId'] == account_id:
            return account['value']

if __name__ == '__main__':
    #Enter your test credentials here
    email = ''
    password = ''
    account_id = 12345
    print get_balance(email, password, account_id)
