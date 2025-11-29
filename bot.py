import asyncio
import random
import datetime
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import aiohttp

TELEGRAM_TOKEN = "7524299190:AAHN4syv80fO-YIIvmhee_Q3_9NWBw2vIOE"

# Plataformas alternando
PLATAFORMAS = [
    {
        "nome": "ApostaA7",
        "link": "https://apostaa7.bet/register?code=S6ASLRYE2W"
    },
    {
        "nome": "DD9",
        "link": "https://dd9.bet/register?code=8JNA43OKM6"
    }
]

# Emojis aleatórios
EMOJIS = ["🔥", "💰", "⚡", "🎯", "📊", "🚀", "💎"]

# 3 modelos de sinais
MODELOS_SINAL = [
    "{emoji} Entrada confirmada para {plataforma}! {emoji}\nHorário: {horario}\nModo: {modo}\nAcesse: {link}",
    "{emoji} Sinal encontrado na ***{plataforma}***!\n🕒 {horario}\n⚙ Modo: {modo}\n🔗 {link}",
    "🚀 Oportunidade detectada!\nPlataforma: {plataforma}\n⏰ {horario}\n⚙ Modo: {modo}\n👉 {link}"
]

# Variáveis de controle
rodando = False
tarefa_loop = None


async def enviar_imagem(bot: Bot, chat_id: int):
    """Gera e envia uma imagem usando IA."""
    url = "https://picsum.photos/600/400"  # imagem aleatória
    await bot.send_photo(chat_id=chat_id, photo=url)


async def gerar_sinal():
    """Gera o texto do sinal."""
    plataforma = random.choice(PLATAFORMAS)
    emoji = random.choice(EMOJIS)
    modelo = random.choice(MODELOS_SINAL)
    modo = random.choice(["NORMAL", "TURBO"])

    horario = (datetime.datetime.now() + datetime.timedelta(minutes=random.randint(1, 5))).strftime("%H:%M")

    texto = modelo.format(
        emoji=emoji,
        plataforma=plataforma["nome"],
        horario=horario,
        modo=modo,
        link=plataforma["link"]
    )
    return texto


async def loop_sinais(app, chat_id):
    """Loop automático entre 8 e 12 minutos."""
    global rodando

    while rodando:
        bot = app.bot
        texto = await gerar_sinal()

        await enviar_imagem(bot, chat_id)
        await bot.send_message(chat_id=chat_id, text=texto)

        espera = random.randint(8, 12) * 60
        await asyncio.sleep(espera)


async def start_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global rodando, tarefa_loop
    if rodando:
        await update.message.reply_text("O bot já está rodando! 🔁")
        return

    rodando = True
    chat_id = update.message.chat_id

    await update.message.reply_text("🚀 Iniciando sinais automáticos entre 8 e 12 minutos!")

    tarefa_loop = asyncio.create_task(loop_sinais(context.application, chat_id))


async def stop_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global rodando
    rodando = False
    await update.message.reply_text("🛑 Sinais automáticos pausados.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global rodando
    if rodando:
        await update.message.reply_text("📡 O bot está ativo e enviando sinais!")
    else:
        await update.message.reply_text("⛔ O bot está parado no momento.")


async def next_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.application.bot
    chat_id = update.message.chat_id

    await enviar_imagem(bot, chat_id)
    await bot.send_message(chat_id=chat_id, text=await gerar_sinal())


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start_auto", start_auto))
    app.add_handler(CommandHandler("stop_auto", stop_auto))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("next", next_signal))

    app.run_polling()


if __name__ == "__main__":
    main()
