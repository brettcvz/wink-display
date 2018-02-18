from plaid import Client
from datetime import date

def make_client(client_id, secret, public_key, env="development"):
    return Client(client_id=client_id,
            secret=secret,
            public_key=public_key,
            environment=env)

def get_this_month_transactions(client, access_token):
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    response = client.Transactions.get(access_token,
            start_date=start_of_month.strftime("%Y-%m-%d"),
            end_date=today.strftime("%Y-%m-%d"))
    transactions = response['transactions']

    # the transactions in the response are paginated, so make multiple calls while increasing the offset to
    # retrieve all transactions
    while len(transactions) < response['total_transactions']:
        response = client.Transactions.get(access_token,
                start_date=start_of_month.strftime("%Y-%m-%d"),
                end_date=today.strftime("%Y-%m-%d"),
                offset=len(transactions))
	transactions.extend(response['transactions'])
    return transactions

def get_this_month_spend(client, access_token):
    transactions = get_this_month_transactions(client, access_token)
    spend = 0
    for t in transactions:
        #Don't count certain things towards spend
        if t["name"] == "TRAVEL CREDIT $300/YEAR":
            continue
        if t["name"] == "Payment Thank You - Web":
            continue

        spend += t["amount"]
    return spend

if __name__ == '__main__':
    plaid_client = make_client(
            "PLAID_CLIENT_ID",
            "PLAID_SECRET",
            "PLAID_PUBLIC_KEY")

    credit_card_access_token = "Get via plaid link"
    print get_this_month_spend(plaid_client, credit_card_access_token)
