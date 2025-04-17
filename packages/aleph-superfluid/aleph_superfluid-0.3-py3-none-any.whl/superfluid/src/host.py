from typing import Optional, Type

from web3 import Web3
from web3.contract.contract import ContractFunction
from web3.middleware import ExtraDataToPOAMiddleware

from .constants import HOST_ABI
from .operation import Operation
from .types import BatchOperationType


class Host:

    def __init__(self, rpc: str, host_address: str) -> None:
        self.rpc = rpc
        web3 = Web3(Web3.HTTPProvider(rpc))
        web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        self.contract = web3.eth.contract(
            address=host_address, abi=HOST_ABI)

    def call_agreement(self, agreement_address: str, calldata: str, user_data: str) -> Operation:
        try:
            agreement_call: ContractFunction = self.contract.functions.callAgreement(
                agreement_address, calldata, user_data)
            return Operation(self.rpc, agreement_call, BatchOperationType.SUPERFLUID_CALL_AGREEMENT)
        except Exception as e:
            raise e

    def call_app_action() -> Operation:
        pass
