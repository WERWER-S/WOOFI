from client import Client
from utils import accounts, sleeping
from config import POVTOR, Min_Akaunt, Max_Akaunt
from tasks.woofi import WooFi
from termcolor import cprint
from models import Arbitrum, Avalanche, Polygon, Fantom, Optimism, BSC
from web3.middleware import geth_poa_middleware
import random


def swap_to_usdt(chain, value):
    max_accaunts = accounts.__len__()
    number_accounts = 0
    value_old = value

    for account in accounts:
        random_ = random.randint(1, 20)  # разброс +-10%
        value = value_old * (110 - random_) / 100

        number_accounts += 1

        retry = 0
        vihod = False
        while not vihod:
            try:
                client = Client(private_key=account, network=chain)
                client.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
                woofi = WooFi(client=client)
                tx = woofi.swap_coin_to_usdt(value=value)
                res = client.verif_tx(tx_hash=tx)
                if res:
                    vihod = True
            except Exception as err:
                retry += 1
                cprint(f'[{client.address}] swap error: {type(err).__name__} {err}', 'red')
                if retry < POVTOR:
                    cprint(f'[{retry}/{POVTOR}] trying again...', 'yellow')
                    sleeping(15, 15)
                else:
                    vihod = True

        rnd_time = random.randint(Min_Akaunt, Max_Akaunt)  # время между аккаунтами
        if number_accounts < max_accaunts:
            print(f"Сон {rnd_time} секунд до {number_accounts + 1}/{max_accaunts} аккаунта\t")
            sleeping(rnd_time, rnd_time)


if __name__ == '__main__':
    while True:
        cprint('Выбери сеть откуда заправляем: ','blue')
        print('1. BSC')
        print('2. Avalanche')
        print('3. Polygon')
        cprint('0. Закончить работу', 'red')
        nomer_from_chain = input('Номер сети: ')
        if nomer_from_chain == '0':
            break
        elif nomer_from_chain == 1:
            from_chain = BSC
        elif nomer_from_chain == 2:
            from_chain = Avalanche
        else:
            from_chain = Polygon

        cprint(f'Сейчас надо будет ввести количество. Оно вводится в количестве нативного токена сети источника. Если это BSC, то, например, "0.01". И он возьмет 0.01 BNB. Разброс будет +-10%. Чтобы не палиться, минималки бери на сайте.', 'yellow')
        count = float(input('Количество нативного токена источника: '))

        swap_to_usdt(from_chain, count)

    print("Скрипт закончил работу.")