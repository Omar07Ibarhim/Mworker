import os
import subprocess
import random
import time
from datetime import datetime
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


# Определяем константы для настроек таймера
CONFIG_FILE = 'config.json'
config = {}


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {
            'pomodoro_duration': 25 * 60,
            'short_break_duration': 5 * 60,
            'long_break_duration': 15 * 60,
            'pomodoro_cycles': 4,
            'sound_notifications_enabled': True,
            'directory': None,
            'music_file': "background_music.mp3"
        }
        save_config(config)
    return config


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
        f.flush()  # Добавить эту строку


config = load_config()
POMODORO_DURATION = config['pomodoro_duration']
SHORT_BREAK_DURATION = config['short_break_duration']
LONG_BREAK_DURATION = config['long_break_duration']
POMODORO_CYCLES = config['pomodoro_cycles']
SOUND_NOTIFICATIONS_ENABLED = config['sound_notifications_enabled']
DIRECTORY = config.get('directory')
MUSIC_FILE = config.get('music_file')  # Имя файла для фоновой музыки


# Определяем константы для файлов и сообщений
REPORT_FILE_NAME = "pomodoro_report.txt" # Имя файла для отчета
user_FILE = "user_name.txt" # Имя файла для сохранения имени пользователя
INVALID_CHOICE_MESSAGE = "Неверный выбор. Пожалуйста, попробуйте еще раз." # Сообщение для неверного ввода пользователя
TIMER_FINISHED_MESSAGE = "Таймер завершен!" # Сообщение для завершения таймера
TIME_UP_MESSAGE = "Время вышло!" # Сообщение для окончания времени

if DIRECTORY is None or DIRECTORY == "":
    audio_path = MUSIC_FILE
else:
    audio_path = os.path.join(DIRECTORY, MUSIC_FILE)



# Определяем функцию для запуска таймера помидора

def start_pomodoro_timer():
    config = load_config()  # Обновить значения конфигурации
    POMODORO_DURATION = config['pomodoro_duration']
    SHORT_BREAK_DURATION = config['short_break_duration']
    LONG_BREAK_DURATION = config['long_break_duration']
    POMODORO_CYCLES = config['pomodoro_cycles']
    SOUND_NOTIFICATIONS_ENABLED = config['sound_notifications_enabled']
    
    for cycle in range(POMODORO_CYCLES):
        # Работаем в режиме помидора
        start_timer(POMODORO_DURATION)

        # Делаем перерыв после работы, если это не последний цикл
        if cycle < POMODORO_CYCLES - 1:
            if cycle % 4 == 3:
                start_timer(LONG_BREAK_DURATION)
            else:
                start_timer(SHORT_BREAK_DURATION)


# Определяем функцию для запуска таймера с заданной продолжительностью
def start_timer(duration):
    for seconds in range(duration, -1, -1):
        display_time(seconds)
        if SOUND_NOTIFICATIONS_ENABLED:
            time.sleep(1)
    play_notification_sound()
    print(TIMER_FINISHED_MESSAGE)


# Определяем функцию для отображения времени в формате ММ:СС
def display_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    print('\r{:02d}:{:02d} осталось'.format(minutes, seconds), end='', flush=True)

# Определяем функцию для показа уведомления с оставшимся временем или сообщением о его окончании
def show_notification(seconds):
    minutes = seconds // 60
    if minutes == 0 and seconds <= 5:
        notification_text = TIME_UP_MESSAGE
        main_menu()
    else:
        notification_text = '{:02d}:{:02d} осталось'.format(minutes, seconds % 60)
    print(notification_text)

# Определяем функцию для проигрывания звукового сигнала при завершении таймера
def play_notification_sound():
    os.system('play -nq -t alsa synth {} sine {}'.format(1, 440))

# Определяем функцию для генерации отчета о проделанной работе и сохранения его в файл
def generate_report():
    now = datetime.now()
    report_filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    with open(report_filename, 'w') as report_file:
        report_file.write("Pomodoro Report\n")
        report_file.write("Generated at: {}\n\n".format(now.strftime("%Y-%m-%d %H:%M:%S")))
        report_file.write("Pomodoro duration: {} minutes\n".format(POMODORO_DURATION // 60))
        report_file.write("Short break duration: {} minutes\n".format(SHORT_BREAK_DURATION // 60))
        report_file.write("Long break duration: {} minutes\n".format(LONG_BREAK_DURATION // 60))
        report_file.write("Number of cycles: {}\n\n".format(POMODORO_CYCLES))
        report_file.write("Work Sessions:\n")
        for cycle in range(POMODORO_CYCLES):
            report_file.write("Cycle {}: Work\n".format(cycle + 1))
            if cycle < POMODORO_CYCLES - 1:
                if cycle % 4 == 3:
                    report_file.write("Cycle {}: Long Break\n".format(cycle + 1))
                else:
                    report_file.write("Cycle {}: Short Break\n".format(cycle + 1))

# Определяем функцию для отображения главного меню и обработки выбора пользователя
def main_menu():
    while True:
        print("Pomodoro Timer - Main Menu")
        choice = get_user_choice()
        process_user_choice(choice)

# Определяем функцию для получения выбора пользователя из списка возможных действий
def get_user_choice():
    print("1. Start Pomodoro Timer")
    print("2. Generate Report")
    print("3. Display Random Quote")
    print("4. Play Background Music")
    print("5. Stop Background Music")
    print("6. Clear Screen")
    print("7. Settings")
    print("8. Exit")
    choice = input("Enter your choice (1-8): ")
    return choice

# Определяем функцию для выполнения действия в соответствии с выбором пользователя
def process_user_choice(choice):
    clear_screen()
    if choice == '1':
        load_config()
        start_pomodoro_timer()
    elif choice == '2':
        generate_report()
    elif choice == '3':
        display_random_quote()
    elif choice == '4':
        play_background_music()
    elif choice == '5':
        stop_background_music()
    elif choice == '6':
        clear_screen()
    elif choice == '7':
        settings_menu()
    elif choice == '8':
        exit_program()
    else:
        print(INVALID_CHOICE_MESSAGE)

def settings_menu():
    while True:
        print("Pomodoro Timer - Settings Menu")
        print(f"1. Pomodoro duration: {config['pomodoro_duration'] // 60} minutes")
        print(f"2. Short break duration: {config['short_break_duration'] // 60} minutes")
        print(f"3. Long break duration: {config['long_break_duration'] // 60} minutes")
        print(f"4. Pomodoro cycles: {config['pomodoro_cycles']}")
        print(f"5. Sound notifications enabled: {config['sound_notifications_enabled']}")
        print(f"6  Background music settings")
        print(f"7. Back to main menu")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            pomodoro_duration = int(input('Enter pomodoro duration in minutes: '))
            config['pomodoro_duration'] = pomodoro_duration * 60
            save_config(config)
            POMODORO_DURATION = config['pomodoro_duration']
            
        elif choice == '2':
            short_break_duration = int(input('Enter short break duration in minutes: '))
            config['short_break_duration'] = short_break_duration * 60
            save_config(config)
            SHORT_BREAK_DURATION = config['short_break_duration']
            
        elif choice == '3':
            long_break_duration = int(input('Enter long break duration in minutes: '))
            config['long_break_duration'] = long_break_duration * 60
            save_config(config)
            LONG_BREAK_DURATION = config['long_break_duration']
            
       

        elif choice == '4':
            pomodoro_cycles = int(input('Enter number of pomodoro cycles: '))
            config['pomodoro_cycles'] = pomodoro_cycles
            save_config(config)
            POMODORO_CYCLES = config['pomodoro_cycles']
            
        elif choice == '5':
            sound_notifications_enabled = input('Enable sound notifications (y/n): ')
            if sound_notifications_enabled.lower() == 'y':
                config['sound_notifications_enabled'] = True
                save_config(config)
                print('Sound notifications enabled')       

            else:
                config['sound_notifications_enabled'] = False
                save_config(config)
                print('Sound notifications disabled')

        elif choice == '6':
            directory = input("directory")
            music_file = input("file name example.mp3")
            config['directory'] = directory
            config['music_file'] = music_file
            save_config(config)






             

        elif choice == '7':
            clear_screen()
            main_menu()        

        

# Определяем функцию для отображения случайной цитаты из списка
def display_random_quote():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt"
    ]
    quote = random.choice(quotes)
    print("Random Quote of the Day:\n{}".format(quote))
#pygame запуст фона
def play_background_music():
    pygame.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()



# Определяем функцию для остановки фоновой музыки
def stop_background_music():
    
    pygame.mixer.music.stop()


# Определяем функцию для получения имени пользователя от него же
def get_user_name():
    name = input("Enter your name: ")
    return name

# Определяем функцию для приветствия пользователя по имени
def greet_user(name):
    print("Welcome, {}! Let's boost your productivity with the Pomodoro Timer.".format(name))

# Определяем функцию для сохранения имени пользователя в файл
def save_user_name(name):
    with open(user_FILE, "w") as file:
        file.write(name)

# Определяем функцию для загрузки имени пользователя из файла, если он существует, иначе возвращаем None
def load_user_name():
    try:
        with open(user_FILE, "r") as file:
            name = file.readline()
            return name.strip()
    except FileNotFoundError:
        return None
    
# Определяем функцию для настройки программы: загружаем или запрашиваем имя пользователя, приветствуем его и сохраняем его имя в файл
def setup():
    name = load_user_name()
    if name is None:
        name = get_user_name()
        save_user_name(name)
    greet_user(name)

# Определяем функцию для запуска главного меню
def main():
    setup()
    main_menu()

# Определяем функцию для выхода из программы
def exit_program():
    print("Exiting...")
    os.sys.exit()

# Определяем функцию для очистки экрана в зависимости от операционной системы
def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

# Вызываем главную функцию, если программа запущена как основной модуль
if __name__ == '__main__':
    main()

