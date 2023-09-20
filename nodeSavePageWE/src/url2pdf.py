import os
import time
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types, executor
bot = Bot(token='TOKEN')
dp = Dispatcher(bot)
import subprocess

@dp.message_handler(commands=['start', 'go'])
async def start_handler(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Сохраняю страницы в пдф, ограничение 20 мб')


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_file3(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    try:
        await bot.send_message(chat_id, 'Получаю заголовок')
        time.sleep(1)
        reqs = requests.get(text, headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; MAR-LX1H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.4103.106 Mobile Safari/537.36'})
        soup = BeautifulSoup(reqs.text, 'html.parser')
        for title in soup.find_all('title'):
            a = (title.get_text())
        await bot.send_message(chat_id, a)
    except:
        await bot.send_message(chat_id, 'Получить заголовок не удалось')

    try:
        filename = time.strftime("%d-%m-%Y_%H-%M-%S")
        await bot.send_message(chat_id, 'Скачиваю страницу')
        time.sleep(1)
        try:
            subprocess.run(["xvfb-run", "wkhtmltopdf", text, f"{filename}.pdf"], check=True)
            subprocess.run(["cp", f"{filename}.pdf", "/home/orangepi/git/url2pdf.github.io/PDF"], check=True)
        except ZeroDivisionError:
            # Обработка ошибки деления на ноль
            await bot.send_message(chat_id, f'Ошибка: не получилось скачать PDF')
        #add var for node
        with open('text.txt', 'w') as file:
            file.write(text)
        with open('filename.txt', 'w') as file:
            file.write(filename)
        with open('a.txt', 'w') as file:
            file.write(a)
        try:
            subprocess.check_call(["node", "test.js"])
        except subprocess.CalledProcessError as e:

            await bot.send_message(chat_id, f'Ошибка: {e.returncode}')


        try:
            subprocess.run(["cp", f"{filename}.html", "/home/orangepi/git/url2pdf.github.io/PDF"], check=True)
            await bot.send_message(chat_id, 'скачиваю html')
        except Exception as eee2:
            await bot.send_message(chat_id, f'Ошибка: {eee2}')

        #add text2html
        with open('/home/orangepi/git/url2pdf.github.io/index.html', 'r', encoding='utf-8') as file:
            existing_content = file.read()
        await bot.send_message(chat_id, 'добавляю текст в Index.html')
        insertion_point = existing_content.find('<div class="card">')

        new_text = f'''
        <div class="card">
            <h2>

                <a href="./PDF/{filename}.pdf" target="_blank">
                    {a}[pdf]<br>
                </a>
        

                <p><a href="{text}" target="_blank">{text}[url]</a></p>
            
            <a href="./PDF/{filename}.html" target="_blank">
                    {a}[html] <br>
            
            </h2>
        </div>
        '''

        modified_content = existing_content[:insertion_point] + new_text + existing_content[insertion_point:]


        with open('/home/orangepi/git/url2pdf.github.io/index.html', 'w', encoding='utf-8') as file:
            file.write(modified_content)


        await bot.send_message(chat_id, 'Конвертирую в PDF')
        time.sleep(2)
        await bot.send_message(chat_id, 'Готовлю к отправке')
        with open(f'{filename}.pdf', 'rb') as document:
            await bot.send_document(chat_id, document)
        time.sleep(2)
        try:
            await bot.send_message(chat_id, f'{a}')
        except:
            pass
        try:
            os.system(f'rm *.pdf')
            os.system(f'rm *.html')
            os.system(f'rm *.txt')
            await bot.send_message(chat_id, 'файлы удалены')
        except:
            await bot.send_message(chat_id, 'Ошибка удаления')
    except Exception as eee1:
        await bot.send_message(chat_id, f'Ошибка: {eee1}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

