import telebot
from PIL import Image, ImageDraw
import base64
from io import BytesIO

# --- TOKEN DO BOT NOVO ---
TOKEN = "8213585953:AAG48cfeRmkbduaQ1AztWx-qpQWcTt26PYA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def gerar_molde(m):
    # Gera o molde 600x600 do zero
    img = Image.new("RGB", (600, 600), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Desenha a grade preta de 20 em 20 pixels
    for y in range(0, 600, 20):
        for x in range(0, 600, 20):
            draw.rectangle([x, y, x+20, y+20], outline=(0,0,0))

    # Transforma em STRING BASE64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Manda o arquivo TXT com o código para você copiar
    with open("molde_lira.txt", "w") as f:
        f.write(f"data:image/png;base64,{b64_str}")
    
    bot.send_document(m.chat.id, open("molde_lira.txt", "rb"), caption="📄 Código Base64 pronto!")
    bot.send_photo(m.chat.id, buffer.getvalue(), caption="✅ Visualização do Molde")

print("🚀 Bot Lira Base64 Online!")
bot.infinity_polling()
