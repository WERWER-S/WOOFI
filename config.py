import os
from pathlib import Path

# Создаем объект Path для директории
directory_path = Path("C:/Users/Kirill/Desktop/Project/Web3")

absolute_path = directory_path.absolute()

ABIS_DIR = os.path.join(absolute_path, 'abis')

TOKEN_ABI = os.path.join(ABIS_DIR, 'token.json')
WOOFI_ABI = os.path.join(ABIS_DIR, 'woofi.json')
STARGATE_ABI = os.path.join(ABIS_DIR, 'stargate.json')
BALANCER_ABI = os.path.join(ABIS_DIR, 'balancer.json')

POVTOR = 3
Min_Akaunt = 30 #время между аккаунтами
Max_Akaunt = 60
