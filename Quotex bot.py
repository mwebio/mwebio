import telegram
import requests
import json
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram Bot Token
TELEGRAM_TOKEN = '6406472622:AAEh27NIJMTWP-a5aTxgFSGeIXbNDJnuvLs'

# Quotext API endpoint
QUOTEXT_API_URL = 'https://api.quotext.com'

# Initialize Telegram Bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

def extract_trade_signals_from_text(message):
    # Implement logic to extract trade signals from text message
    pattern = r'(\d{2}:\d{2}) - (\w+-\w+) - (PUT|CALL|UP|DOWN)\s*✅?'
    match = re.findall(pattern, message)
    
    signals = []
    if match:
        for m in match:
            time = m[0]
            currency = m[1]
            option = m[2]
            entry_price = 0  # Default entry price
            
            # Logic for determining entry price based on opening and closing prices
            if option == 'PUT' or option == 'DOWN':
                entry_price = 1  # If opening price < closing price, use $1 as entry price
            elif option == 'CALL' or option == 'UP':
                entry_price = 1  # If opening price > closing price, double the previous entry price
            
            # Append trade signal to the list
            signals.append({'time': time, 'currency': currency, 'option': option, 'entry_price': entry_price})
    
    return signals

def extract_trade_signals_from_image(image):
    # Implement logic to extract trade signals from image
    # You may use OCR (Optical Character Recognition) libraries to extract text from the image
    pass

def extract_trade_signals(message):
    # Check if the message contains text or image
    if message.text:
        return extract_trade_signals_from_text(message.text)
    elif message.photo:
        return extract_trade_signals_from_image(message.photo[-1])  # Use the last photo (highest resolution)
    else:
        return []

def execute_trade(signal, email, password, use_demo=False):
    try:
        # Use Quotext API to execute the trade based on the signal
        # Send a POST request to the Quotext API with the trade details and authentication
        trade_data = {
            'symbol': signal['currency'],
            'action': 'buy' if signal['option'] in ['CALL', 'UP'] else 'sell',  # Mapping option to action
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
    except Exception as e:
        # Log error if trade execution fails
        logging.error('Error executing trade: %s', e)

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
