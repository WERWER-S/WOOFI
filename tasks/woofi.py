from web3 import Web3
from loguru import logger
from typing import Optional
import time

from client import Client
from config import WOOFI_ABI
from utils import read_json
from models import TokenAmount
from models import BSC, Avalanche, Polygon


class WooFi:

    def __init__(self, client: Client):
        self.client = client

        if self.client.network == BSC:
            self.usdt_address = Web3.to_checksum_address("0x55d398326f99059fF775485246999027B3197955")
            self.router_address = Web3.to_checksum_address('0x4f4Fd4290c9bB49764701803AF6445c5b03E8f06')
            self.decimals = 18
        if self.client.network == Avalanche:
            self.usdt_address = Web3.to_checksum_address("0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7")
            self.router_address = Web3.to_checksum_address('0xc22fbb3133df781e6c25ea6acebe2d2bb8cea2f9')
            self.decimals = 6
        if self.client.network == Polygon:
            self.usdt_address = Web3.to_checksum_address("0xc2132D05D31c914a87C6611C10748AEb04B58e8F")
            self.router_address = Web3.to_checksum_address('0x817Eb46D60762442Da3D931Ff51a30334CA39B74')
            self.decimals = 6

    native_coin_address = Web3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE')
    router_abi = read_json(WOOFI_ABI)

    def swap_coin_to_usdt(self, value: [int | float | str], slippage: float = 1):
        contract = self.client.w3.eth.contract(
            abi=WooFi.router_abi,
            address=self.router_address
        )
        amount = TokenAmount(value)
        coin_price = self.client.get_eth_price(token=self.client.network.coin_symbol)
        min_to_amount = TokenAmount(
            amount=coin_price * float(amount.Ether) * (1 - slippage / 100),
            decimals=self.decimals
        )
        try:
            tx = self.client.send_transaction(
                to=self.router_address,
                data=contract.encodeABI('swap',
                                        args=(
                                            WooFi.native_coin_address,
                                            self.usdt_address,
                                            amount.Wei,
                                            min_to_amount.Wei,
                                            self.client.address,
                                            self.client.address
                                        )),
                value=amount.Wei
            )
            success_tx = self.client.verif_tx(tx)

            if success_tx:
                logger.info(f"{self.client.network.explorer}tx/{tx.hex()}")
                logger.success(f'[{self.client.address}][Woofi Swap] Successfully swap to USDT')
            else:
                logger.error(f'[{self.client.address}][Woofi Swap] swap error to USDT')
        except Exception as err:
            logger.error(f'[{self.client.address}][Woofi Swap] swap error to USDT: {type(err).__name__} {err}')

    def swap_usdt_to_coin(self, amount: Optional[TokenAmount] = None, slippage: float = 1):
        if not amount:
            amount = self.client.balance_of(contract_address=self.usdt_address)

        res = self.client.approve(
            token_address=self.usdt_address,
            spender=self.router_address,
            amount=amount
        )

        if not res:
            return False
        time.sleep(20)

        contract = self.client.w3.eth.contract(
            abi=WooFi.router_abi,
            address=self.router_address
        )

        coin_price = self.client.get_eth_price(token=self.client.network.coin_symbol)
        min_to_amount = TokenAmount(
            amount=float(amount.Ether) / coin_price * (1 - slippage / 100)
        )

        try:
            tx = self.client.send_transaction(
                to=self.router_address,
                data=contract.encodeABI('swap',
                                        args=(
                                            self.usdt_address,
                                            WooFi.native_coin_address,
                                            amount.Wei,
                                            min_to_amount.Wei,
                                            self.client.address,
                                            self.client.address,
                                        ))
            )

            success_tx = self.client.verif_tx(tx)

            if success_tx:
                logger.info(f"https://opbnbscan.com/tx/{tx.hex()}")
                logger.success(f'[{self.client.address}][opBNB Bridge] Successfully bridge to opBNB')
            else:
                logger.error(f'[{self.client.address}][opBNB Bridge] bridge error to opBNB')
        except Exception as err:
            logger.error(f'[{self.client.address}][opBNB Bridge] bridge error to opBNB: {type(err).__name__} {err}')