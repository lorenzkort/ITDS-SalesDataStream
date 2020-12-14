import requests
import time

def telegram_send_text(bot_message='Hey this is a text message', chat_id = '-459671235'): #ITDS Sales Chat
    
    bot_token = '1199446442:AAFBl87U1LEwtlwby0LFSdybzYAgu16NrSk'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    time.sleep(1)

    return response.json()

# https://api.telegram.org/bot1199446442:AAFBl87U1LEwtlwby0LFSdybzYAgu16NrSk/getUpdates

if __name__ == '__main__':
    start = time.time()
    telegram_send_text('Vacturebot test', '-381451433')
    print(round(time.time() - start, 2))