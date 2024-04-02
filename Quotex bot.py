import telegram
import requests
import json
import re
import logging
from ratelimit import limits, sleep_and_retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram Bot Token
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Quotext API endpoint
QUOTEXT_API_URL = 'https://api.quotext.com'

# Initialize Telegram Bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Rate limit settings (10 requests per minute)
RATE_LIMIT = 10
RATE_LIMIT_PERIOD = 60

@sleep_and_retry
@limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD)
def execute_trade(signal, email, password, use_demo=False):
    try:
        # Determine trade action based on profit or loss
        if signal['entry_price'] > 1:
            action = 'buy' if signal['option'] in ['CALL', 'UP'] else 'sell'  # If profit, execute buy/sell
        else:
            action = 'sell' if signal['option'] in ['CALL', 'UP'] else 'buy'  # If loss, execute sell/buy

        # Use Quotext API to execute the trade based on the signal
        # Send a POST request to the Quotext API with the trade details and authentication
        trade_data = {
            'symbol': signal['currency'],
            'action': action,
            'price': signal['entry_price'],
            # Add any other necessary parameters for the trade
            'email': email if not use_demo else 'mwebilevis40@gmail.com',  # Use demo account email if specified
            'password': password if not use_demo else '106281Levis'  # Use demo account password if specified
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{QUOTEXT_API_URL}/execute_trade', headers=headers, data=json.dumps(trade_data))
        
        # Check response status code
        response.raise_for_status()
        
        # Log trade execution
        logging.info('Trade executed successfully: %s', response.json())
    except requests.exceptions.HTTPError as e:
        logging.error('HTTP error occurred: %s', e)
    except requests.exceptions.ConnectionError as e:
        logging.error('Error connecting to Quotext API: %s', e)
    except requests.exceptions.Timeout as e:
        logging.error('Timeout occurred while connecting to Quotext API: %s', e)
    except requests.exceptions.RequestException as e:
        logging.error('An error occurred while sending the request to Quotext API: %s', e)
    except Exception as e:
        # Log any other unhandled exceptions
        logging.error('An unexpected error occurred during trade execution: %s', e)
    else:
        # Successful trade execution, no need to count towards rate limit
        pass

def main():
    try:
        # Set the IDs of the Telegram channels you want to monitor
        CHANNEL_IDS = ['1001925847841', '1002078184249', '1001940077808', '1001641305863', '1002080782605', '1001820088359', '1002079856682']

        # Your Quotext login credentials
        email = 'mwebilevis40@gmail.com'
        password = '106281Levis'

        # Continuously listen for new messages in the specified channels
        for channel_id in CHANNEL_IDS:
            for update in bot.get_updates():
                if update.message and str(update.message.chat_id) == channel_id:
                    message = update.message
                    trade_signals = extract_trade_signals(message)
                    if trade_signals:
                        for signal in trade_signals:
                            # Execute trade using the appropriate account (demo or main)
                            execute_trade(signal, email, password, use_demo=True)
    except Exception as e:
        # Log any unhandled exceptions
        logging.error('An error occurred: %s', e)

if __name__ == "__main__":
    main()
