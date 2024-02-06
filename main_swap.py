from client import Client
from utils import accounts, sleeping
from loguru import logger
from tasks.woofi import WooFi
from models import Arbitrum, Avalanche, Polygon, Fantom, Optimism, BSC
from web3.middleware import geth_poa_middleware
import random


def swap(chain, value, parametrs, nomer_puti):
    max_acconts = len(accounts)
    parametrs['max_acconts'] = max_acconts

    count_max = parametrs['count_max']
    count_min = parametrs['count_min']

    if chain == 1:
        chain = Avalanche
    elif chain == 2:
        chain = Polygon
    else:
        chain = BSC

    for current_tranz in range(0, count_max):
        logger.info(f'Транзакция: {current_tranz + 1}/{count_max}')
        current_account = 0

        for account in accounts:
            value_old = value
            random_ = random.randint(1, 20)  # разброс +-10%
            value = value_old * (110 - random_) / 100

            client = Client(private_key=account, network=chain)
            client.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            current_account += 1
            parametrs['current_account'] = current_account

            if (current_tranz + 1) > random.randint(count_min, count_max):  # проверка на кол-во
                continue

            if nomer_puti == 1:
                woofi = WooFi(client=client)
                woofi.swap_coin_to_usdt(value=value)

            elif nomer_puti == 2:
                pass

            sleeping()
        sleeping(45, 60)
