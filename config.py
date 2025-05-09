from pathlib import Path 
import sys


# =================CONFIG=================
BASE_DIR = Path(getattr(sys, '_MEIPASS', Path(sys.argv[0]).parent)).resolve()  #===> Это нужно когда .py преобразован в .exe

# DEFAULT_JSON_NAME = "stats.json"