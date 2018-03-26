from fints.client import FinTS3PinTanClient
import fints_url
import os
import pprint
from datetime import date, timedelta
from uwsgidecorators import timer

from bankthing.db import make_session
from bankthing.models import Account, Balance, Transaction

import bankthing.config
BANK_CODE = os.environ['BANK_CODE']
BANK_USERNAME = os.environ['BANK_USERNAME']
BANK_PIN = os.environ['BANK_PIN']
BANK_URL = fints_url.find(bank_code=BANK_CODE)


db = make_session()


@timer(30 * 60)
def fetch_bank_data(num: int):
    fints = FinTS3PinTanClient(
        BANK_CODE,
        BANK_USERNAME,
        BANK_PIN,
        BANK_URL,
    )

    accounts_f = fints.get_sepa_accounts()
    for account_f in accounts_f:
        account = db.query(Account).filter(Account.iban == account_f.iban).first()
        if not account:
            account = Account(account_f.iban, account_f.bic)
            db.add(account)
            db.flush()

        balance_f = fints.get_balance(account_f)
        balance = Balance(balance_f.amount.amount,
                          balance_f.amount.currency,
                          account)
        db.add(balance)
        db.flush()

        # statements = fints.get_statement(account, date.today() - timedelta(days=30), date.today())
        # pprint.pprint(balance)
        # for statement in statements:
        #     pprint.pprint(statement.data)

    db.commit()
