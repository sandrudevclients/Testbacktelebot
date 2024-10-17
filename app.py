import telebot
import g4f
import streamlit as st
import threading

# Замените 'YOUR_API_TOKEN' на токен вашего бота
API_TOKEN = '7265689337:AAE_CV6L5ueVTxCzFtKQnK0XeISz1jQeiMY'
bot = telebot.TeleBot(API_TOKEN)

# Флаг для управления работой бота
running = True

def start_bot():
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": message.text}]
            )
            
            if isinstance(response, dict) and 'choices' in response:
                if len(response['choices']) > 0 and 'message' in response['choices'][0]:
                    reply_text = response['choices'][0]['message']['content']
                    bot.send_message(message.chat.id, reply_text)
                else:
                    bot.send_message(message.chat.id, "Неверный формат ответа от ИИ.")
            else:
                bot.send_message(message.chat.id, response)
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
            print(f"Ошибка: {str(e)}")

    # Запускаем бота
    bot.polling(none_stop=True)

# Запускаем поток для бота
threading.Thread(target=start_bot).start()

# Интерфейс Streamlit
st.title("Telegram Bot with Streamlit")
st.write("Бот работает в фоновом режиме. Проверьте Telegram для взаимодействия.")

if st.button("Остановить бота"):
    running = False
    st.write("Бот остановлен.")
