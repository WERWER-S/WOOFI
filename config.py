import os
import sys
from pathlib import Path

# Создаем объект Path для директории
if getattr(sys, 'frozen', False):
    directory_path = Path(sys.executable).parent.absolute()
else:
    directory_path = Path(__file__).parent.parent.absolute()

# Here edit your path if you have errors
ABIS_DIR = os.path.join(directory_path, 'woofi', 'abis')

TOKEN_ABI = os.path.join(ABIS_DIR, 'token.json')
WOOFI_ABI = os.path.join(ABIS_DIR, 'woofi.json')

RETRY = 3

PAUSA_MAX = 30 # сон
PAUSA_MIN = 10
