import requests
import time
import os
from environs import Env

env = Env()  
env.read_env() 
                          
bot_token = env('BOT_TOKEN')
API_URL = 'https://api.telegram.org/bot'
TEXT = 'Тестирую ботика'
MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int

while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{bot_token}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{API_URL}{bot_token}/sendMessage?chat_id={chat_id}&text={TEXT}')

    time.sleep(1)
    counter += 1