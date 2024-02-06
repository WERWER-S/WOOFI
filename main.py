from sys import stderr
from main_swap import swap
from loguru import logger

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <3}</level> | <level>{message}</level>")

if __name__ == '__main__':
    while True:
        print('Выбери действие: ')
        print('1. Swap to USDT')
        print('1. Swap from USDT | в разработке')
        print('0. Закончить работу')

        nomer_puti = int(input('Номер действия: '))

        if nomer_puti == 1:

            print('Выбери действие сеть: ')
            print('1. Avalanche')
            print('2. Polygon')
            print('3. BSC')

            chain = int(input('Введите сеть: '))

            print('Количество в нативной монете: ')

            value = float(input('Количество: '))

            parametrs = {
                'count_min': 1,
                'count_max': 1,
            }

            swap(chain, value, parametrs, nomer_puti)

        if nomer_puti == 2:
            pass

        else:
            break

    print("Скрипт закончил работу!!!")