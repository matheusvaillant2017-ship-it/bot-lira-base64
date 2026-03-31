import telebot
import requests
import base64
from io import BytesIO
from PIL import Image

# Coloque o seu TOKEN aqui
bot = telebot.TeleBot("SEU_TOKEN_AQUI")

@bot.message_handler(commands=['gerar'])
def gerar_imagem(message):
    query = message.text.replace("/gerar ", "")
    if not query:
        bot.reply_to(message, "Mande o que você quer gerar. Ex: /gerar lobo")
        return

    bot.send_message(message.chat.id, f"🎨 Gerando '{query}' e convertendo...")

    try:
        # Gerando imagem de servidor livre (ilimitado)
        img_url = f"https://pollinations.ai/p/{query.replace(' ', '_')}?width=512&height=512&seed=42"
        response = requests.get(img_url)
        
        # Converte a imagem recebida em Base64
        img = Image.open(BytesIO(response.content))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Cria o arquivo .txt com o código Base64
        with open("codigo.txt", "w") as f:
            f.write(img_base64)

        # Envia o arquivo para você no Telegram
        with open("codigo.txt", "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ Tá aí o Base64 ilimitado!")

    except Exception as e:
        bot.reply_to(message, f"Deu ruim: {e}")

bot.polling()

