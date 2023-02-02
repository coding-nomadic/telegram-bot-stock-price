import time
import yaml
import requests
import logging
from appconfig import AppConfig
from jugaad_data.nse import NSELive
properties_file = 'config.yml'


# setting up logging with format
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO)

logger = logging.getLogger()

def get_stock_price(stock_name):
     nse = NSELive()
     quote = nse.stock_quote(stock_name)
     logger.info(quote['priceInfo'])
     return quote['priceInfo']

# sending notification to telegram bot
def send_message_to_telegram_bot(bot_token, chat_id,mf_price):
    base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text="
    message = f'{mf_price}'
    url = base_url + message
    try:
        requests.get(url)
    except Exception as error:
        logger.info(f'Error while sending to telegram bot ', error)


# load yml file as object
def load_configuration():
    #setup_logging()
    config = AppConfig(properties_file)
    if config.is_valid is False:
        return
    else:
        return config


if __name__ == '__main__':
    logger.info(f'loading yml file ...!')
    app_config = load_configuration()
    while True:
        mf_price = get_stock_price(app_config.stock_name)
        logger.info(f'Sending request to Telegram API for the notification to bot..')
        send_message_to_telegram_bot(app_config.bot_token, app_config.chat_id,mf_price)
        time.sleep(app_config.interval)
        logger.info(f'sending notification to Telegram after every second ')
