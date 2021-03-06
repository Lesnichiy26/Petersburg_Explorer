import datetime
import os
import random
import string

import vk_api
from dotenv import load_dotenv
from pyowm import OWM
from pyowm.utils.config import get_default_config
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from data.db_session import create_session

load_dotenv(dotenv_path='data/.env')
TOKEN = os.getenv('VK_TOKEN')
API = os.getenv('VK_API')

bad_words = ['какашка', 'тупой', 'дибил', 'даун', 'чмо']
hello_words = ['привет', 'хай', 'здарова', 'салам', 'салют', 'челси']
bye_words = ['пока', 'до свидания', 'бб']
yes_words = ['да', 'конечно', 'абсолютно', 'верно', 'точно']
no_words = ['нет']
how_are_u_words = ['как дела', 'как жизнь', 'все хорошо']

now = datetime.datetime.now()


def bot():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    group_id = int(os.environ["VK_GROUP_ID"])
    longpoll = VkBotLongPoll(vk_session, group_id)

    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = vk.users.get(user_id=event.obj.message['from_id'], fields=["city"])
            first_name = response[0]["first_name"]
            if event.obj.message['text'].lower().rstrip(string.punctuation).strip() == 'команды':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"1. Сайт \n"
                                         f"2. Информация\n"
                                         f"3. Время \n"
                                         f"4. Дата \n"
                                         f"5. Погода \n"
                                         f"Также вы можете немного поговорить с ним, используя обычные фразы.",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() == 'сайт':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"petersburg-explorer.ru \n",
                                 random_id=random.randint(0, 2 ** 64))
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Если ВКонтакте не открывает ссылку, то просто вставьте ее в браузер",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() == 'информация':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Petersburg Explorer - это новая игра о Санкт-Петербурге. Вы погружаетесь в северную столицу России благодаря панорамам Яндекс карт. \n \n"
                                         "В процессе игры вы будете гулять по городу. Вам нужно будет дойти до определённого места. "
                                         "Чем ближе вы придёте к месту назначения, тем больше очков вы получите! Так что вперёд гулять по нашему любимому городу!",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() == 'дата':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=now.strftime("%d-%m-%Y"),
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation) == 'время':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=now.strftime("%H:%M:%S"),
                                 random_id=random.randint(0, 2 ** 64))
            elif 'погода' in event.obj.message['text'].lower().rstrip(string.punctuation):
                config_dict = get_default_config()
                config_dict['language'] = 'ru'
                owm = OWM(API, config_dict)
                manager = owm.weather_manager()
                observation = manager.weather_at_place('Санкт-Петербург')
                pogoda = observation.weather
                temperature = pogoda.temperature('celsius')['temp']
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Сейчас в городе Санкт-Петербурге " + str(int(temperature)) + " °С",
                                 random_id=random.randint(0, 2 ** 64))

            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in hello_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {first_name}!",
                                 random_id=random.randint(0, 2 ** 64))

            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in bad_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Соблюдайте нормы речевого этикета!",
                                 random_id=random.randint(0, 2 ** 64))

            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in yes_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Хорошо",
                                 random_id=random.randint(0, 2 ** 64))

            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in bye_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Удачи!",
                                 random_id=random.randint(0, 2 ** 64))

            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in how_are_u_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"У меня все хорошо!",
                                 random_id=random.randint(0, 2 ** 64))

            elif 'жалоб' in event.obj.message['text'].lower().rstrip(string.punctuation).strip():
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Вы хотите оставить жалобу на личное рассмотрение разработчиками? (да, нет)",
                                 random_id=random.randint(0, 2 ** 64))
                if 'да' in event.obj.message['text'].lower().strip():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Максимально подробно опишите проблему, прозошедшую с Вами",
                                     random_id=random.randint(0, 2 ** 64))

            #         добавление жалобы в БД

            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{event.obj.message['text'].capitalize().rstrip(string.punctuation)}? Вы уверены? ",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    bot()
