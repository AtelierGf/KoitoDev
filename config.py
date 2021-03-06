import os
from dotenv import find_dotenv,load_dotenv

load_dotenv(find_dotenv())
TW_CONSUMER_KEY=os.environ.get('TW_CONSUMER_KEY')
TW_CONSUMER_SECRET = os.environ.get('TW_CONSUMER_SECRET')
TW_TOKEN = os.environ.get('TW_TOKEN')
TW_TOKEN_SECRET = os.environ.get('TW_TOKEN_SECRET')
USER = os.environ.get('USER')
MECAB_DIC_PATH = os.environ.get('MECAB_DIC_PATH')
REPLY_LOG_PATH = os.environ.get('REPLY_LOG_PATH')
