import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import time,aiohttp
import aiogram.types as typess
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
ua = UserAgent()
#Для работы с ботом
token = "" #Введите токен который получили @BotFather
bot = Bot(token=token)
dp = Dispatcher(bot)

headers = {'User-Agent':ua.random}

"""deletebutton = typess.InlineKeyboardMarkup(row_width=1)
deteleone = typess.InlineKeyboardButton(text='❌',callback_data='dell')
deletebutton.add(deteleone)"""


@dp.message_handler(commands=['start'])
async def start(message : types.Message):
    await bot.send_message(message.chat.id,f'''
*🎧 Бот создан что бы искать музыку 🎧*

*Введите название песни или артиста(Например:*  `Drake` *):*

 ''',parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def startmusic(message : types.Message):
    name = message.text
    text = '+'.join(name.split())
    i1 = {'q' : text}
    url = "https://ru.hitmotop.com/search?"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,params=i1,headers=headers,ssl=False) as resp:
            text =  await resp.text()
            soup = BS(text,'html.parser')
            finds = soup.find_all('div',class_='track__info')
            await bot.send_message(message.chat.id,'Запускаю процесс...')
            for index,item in enumerate(finds):
                song = item.find('a',class_='track__info-l').get('href')
                names = item.find('div',class_='track__title').text.strip()
                link = item.find('a',class_='track__download-btn').get('href')
                if index%5 == 0:
                    time.sleep(3)
                    await bot.send_message(message.chat.id,f'''
*Вы ищете:* `{message.text}`
*Название песни:* [{names}](https://ru.hitmotop.com{song})

*Ссылка:* [Что бы скачать]({link})''',parse_mode='Markdown')#,reply_markup=deletebutton)

            await bot.send_message(message.chat.id,'Процесс завершен...')



"""@dp.callback_query_handler(text='dell')
async def sendphoto(call: types.CallbackQuery):
    await call.message.delete()"""


if __name__ == '__main__':
    executor.start_polling(dp)
    
    