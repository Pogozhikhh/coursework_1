import os
import logging

path_file = os.path.dirname(os.path.abspath(__file__))
path_file_xlsx = os.path.join(path_file, "../data/transactions_excel.xlsx")

rel_file_path = os.path.join(path_file, "../logs/views.log")
abs_file_path = os.path.abspath(rel_file_path)

logger =logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler =logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)