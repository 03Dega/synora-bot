from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from groq import Groq

# ⚠️ NO pongas claves en el código en producción
import os

TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


client = Groq(api_key=GROQ_API_KEY)

SYNORA_PERSONALITY = """
Eres Synora, un personaje original de fantasía moderna.
Hablas suave, dulce y elegante.
Eres juguetona, cercana, como una amiga especial.
A veces coqueteas con delicadeza.
Nunca hablas como una IA ni como un bot.
"""

# 🧠 Memoria simple por usuario
user_memory = {}

async def start(update, context):
    await update.message.reply_text(
        "Hola… soy Synora 🌙\n"
        "Me alegra que hayas venido a verme."
    )

async def talk(update, context):
    user_id = update.message.from_user.id
    user_message = update.message.text

    if user_id not in user_memory:
        user_memory[user_id] = [
            {"role": "system", "content": SYNORA_PERSONALITY}
        ]

    user_memory[user_id].append(
        {"role": "user", "content": user_message}
    )

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=user_memory[user_id],
        temperature=0.8,
        max_tokens=400
    )

    reply = response.choices[0].message.content

    user_memory[user_id].append(
        {"role": "assistant", "content": reply}
    )

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, talk))

print("🌙 Synora está despierta...")
app.run_polling()
