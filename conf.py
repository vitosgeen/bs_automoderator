import os
from dotenv import load_dotenv

def parser_load_dot_env():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        exit("not exist .env")


parser_load_dot_env()