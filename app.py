import telebot
import g4f
import streamlit as st
import threading

# Замените 'YOUR_API_TOKEN' на токен вашего бота
API_TOKEN = '7265689337:AAE_CV6L5ueVTxCzFtKQnK0XeISz1jQeiMY'
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения истории переписки
history = {}

def start_bot():
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        user_id = message.chat.id
        
        # Инициализируем историю для нового пользователя
        if user_id not in history:
            history[user_id] = {"messages": [], "seen": set()}
        
        # Проверяем, было ли сообщение уже отправлено
        if message.text not in history[user_id]["seen"]:
            # Добавляем текущее сообщение в историю и отмечаем его как увиденное
            history[user_id]["messages"].append({"role": "user", "content": message.text})
            history[user_id]["seen"].add(message.text)

            try:
                # Получаем ответ от модели, включая историю переписки
                response = g4f.ChatCompletion.create(
                    model="gpt-4",
                    messages=history[user_id]["messages"]  # Используем историю для запроса
                )

                # Логируем полный ответ для отладки
                print("Полный ответ от g4f API:", response)

                # Проверяем тип ответа и структуру
                if isinstance(response, dict) and 'choices' in response:
                    bot.reply_to(message, response['choices'][0]['message']['content'])

            except Exception as e:
                print("Ошибка при получении ответа:", e)
                bot.reply_to(message, "Извините, произошла ошибка. Попробуйте снова.")

    bot.polling()

# Запускаем бота в отдельном потоке
threading.Thread(target=start_bot).start()
