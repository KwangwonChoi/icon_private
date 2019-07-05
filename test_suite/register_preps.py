from typing import List

from iconsdk.builder.transaction_builder import TransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet

from .base import Base
import sys
import argparse


class RegisterPrepsTransactions(Base):
    TEST_HTTP_ENDPOINT_URI_V3 = "http://127.0.0.1:9000/api/v3"

    def _make_accounts(self, prep_num):
        return [KeyWallet.create() for _ in range(prep_num)]

    def _make_prep(self, idx):
        return {
                "name": f"banana node{idx}",
                "email": f"banana@banana{idx}.com",
                "website": f"https://banana{idx}.com",
                "details": f"detail{idx}",
                "publicKey": f"0x1234",
                "p2pEndPoint": f"target://{idtest_suitex}.213.123.123:7100"
               }

    def _make_transaction(self, key_wallet):
        return TransactionBuilder(). \
                value(10**20). \
                from_(self._test1.get_address()). \
                to(key_wallet.get_address()). \
                nid(3). \
                nonce(1). \
                step_limit(1000000). \
                version(3). \
                build()

    def _make_account_tx_list(self, addresses: List['KeyWallet']):
        tx_list = []
        for key_wallet in addresses:
            transaction = self._make_transaction(key_wallet)
            signed_transaction = SignedTransaction(transaction, self._test1)
            tx_list.append(signed_transaction)

        return tx_list

    def _make_prep_tx_list(self, accounts):
        tx_list = []
        for i in range(len(accounts)):
            param = self._make_prep(i)
            tx = self.create_register_prep_tx(accounts[i], param, step_limit=10 ** 6)
            tx_list.append(tx)

        return tx_list

    def _register_accounts_tx(self, accounts):
        tx_list = self._make_account_tx_list(accounts)
        return self.process_transaction_bulk(tx_list, self.icon_service)

    def _register_preps_tx(self, accounts):
        tx_list = self._make_prep_tx_list(accounts)
        return self.process_transaction_bulk(tx_list, self.icon_service)

    def _define_system_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', required=True, help='required URL')
        parser.add_argument('-pn', '--preps-num', required=True, help='required number of prep')

        return parser.parse_args()

    def _get_system_args(self, args):
        # get param from command line
        url = args.url
        prep_num = args.pn

        return url, prep_num

    def run(self):
        # define and get system args
        args = self._define_system_args()
        url, prep_num = self._get_system_args(args)

        # make accounts and make transaction
        accounts = self._make_accounts(prep_num)
        _ = self._register_accounts_tx(accounts)

        # make preps and make transaction
        tx_results = self._register_preps_tx(accounts)

        for result in tx_results:
            print(result)


RegisterPrepsTransactions().run()
