import telebot
import requests
import base64
from io import BytesIO
from PIL import Image

# 💢 TOKEN DO LiraBase64_v2_bot
TOKEN = "8213585953:AAG48cfeRmkbduaQ1AztWx-qpQWcTt26PYA"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def boas_vindas(message):
    bot.reply_to(message, "💢 VASCÃO NA ÁREA! \n\nComando: /gerar [descrição]\nExemplo: /gerar um navio pirata realista")

@bot.message_handler(commands=['gerar'])
def gerar_imagem_vasco(message):
    query = message.text.replace("/gerar ", "")
    if not query or query == "/gerar":
        bot.reply_to(message, "⚠️ Escreve o que você quer gerar, porra! Ex: /gerar favela rio de janeiro")
        return

    bot.send_message(message.chat.id, "🎨 O Gigante está criando e convertendo em Base64... Aguarda aí!")

    try:
        # Gerador ILIMITADO e SEM CHAVE
        prompt_final = f"{query}, high quality, cinematic"
        img_url = f"https://pollinations.ai/p/{prompt_final.replace(' ', '_')}?width=512&height=512"
        
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        
        # Converte para Base64 (Texto)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Cria o arquivo de texto
        nome_arquivo = "base64_gerado.txt"
        with open(nome_arquivo, "w") as f:
            f.write(img_base64)

        # Envia o arquivo .txt pro Telegram
        with open(nome_arquivo, "rb") as f:
            bot.send_document(
                message.chat.id, 
                f, 
                caption=f"✅ Base64 da imagem: {query}\n\n💢 CASARÃO!"
            )

    except Exception as e:
        bot.reply_to(message, f"❌ Deu erro: {e}")

bot.polling()
