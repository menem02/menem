import telebot # тут ми потключайм библиотеку телебот 
from telebot.types import Message
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

def detect_image(input_path, model): # ета уже обучиная модель которая можить различить пустини
    np.set_printoptions(suppress=True)
    model = load_model(model, compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(input_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]
    return index, confidence_score





bot = telebot.TeleBot('') # тут ви должни подставить индекс своего бота



@bot.message_handler(commands=['start'])# если напишуть /start то появиться натпись
def start(message: Message):
    bot.send_message(message.chat.id, 'я умею различать пустини') #вот ета


@bot.message_handler(content_types=['photo'])# вот тут будет проверять фото
def photo(message: Message):
    if not message.photo:
        return bot.send_message(message.chat.id, 'ви не скинули картинку')


    file_path = bot.get_file(message.photo[-1].file_id).file_path
    downloaded_file = bot.download_file(file_path)
    with open(f'images/{message.from_user.id}.png', 'wb') as new_file:
        new_file.write(downloaded_file)
    old = bot.send_message(message.chat.id, 'кaртинка получина/')
    index, score = detect_image(f"images/{message.from_user.id}.png", "")# ви должнибудете потставить здесь свой модуль
    bot.delete_message(old.chat.id,old.message_id)
    if index == 0: #  тут оно ишит индекс тех картинак каторих ви обучили в модуле
        bot.send_message(message.chat.id, f'ваша картинка пустиня  с вероятностью {score * 100}%')
    elif index == 1:
        bot.send_message(message.chat.id, f'ваша картинка ледяная пустиня  с вероятностью {score * 100}%')
    else:
        bot.send_message(message.chat.id, f'ваша картинка каминая пустиня  с вероятностью {score * 100}%')




bot.infinity_polling()


