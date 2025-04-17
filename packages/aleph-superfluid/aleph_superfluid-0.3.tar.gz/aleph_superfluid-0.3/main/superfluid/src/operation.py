from typing import Optional

from web3.types import TxParams
from web3.contract.contract import ContractFunction
from web3 import Web3
from eth_typing import HexStr
from eth_account import Account

from .types import BatchOperationType


class Operation:

    def __init__(self, rpc: str, agreement_call: ContractFunction, type: BatchOperationType, forwarder_call: Optional[ContractFunction] = None) -> None:
        self.rpc = rpc
        self.agreement_call = agreement_call
        self.type = type
        self.forwarder_call = forwarder_call

    def exec(self, private_key: str) -> HexStr:
        """
            Signs and broadcasts a transaction
            @param rpc - rpc url
            @param private_key - private key
            @returns - HexStr - The transaction hash
        """
        populated_transaction = self._get_populated_transaction_request(
            self.rpc, private_key)
        web3 = Web3(Web3.HTTPProvider(self.rpc))
        signed_txn = web3.eth.account.sign_transaction(
            populated_transaction, private_key=private_key)
        transaction_hash = web3.eth.send_raw_transaction(
            signed_txn.rawTransaction)
        return transaction_hash.hex()

    def _get_populated_transaction_request(self, rpc: str, private_key: str) -> TxParams:
        """
            Selects and prepares the transaction object to be signed
            @param rpc - rpc url
            @param private_key - private key
            @returns - TxParams - The transaction object
        """
        call = self.forwarder_call if self.forwarder_call is not None else self.agreement_call
        address = Account.from_key(private_key).address
        populated_transaction = call.build_transaction({
            "from": address
        })
        web3 = Web3(Web3.HTTPProvider(rpc))
        nonce = web3.eth.get_transaction_count(address)
        populated_transaction["nonce"] = nonce
        return populated_transaction
