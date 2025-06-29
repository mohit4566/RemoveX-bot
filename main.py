import os
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from rembg import remove
from PIL import Image

TOKEN = os.environ["TOKEN"]  # Railway pe env variable me token daalna hai

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = await update.message.photo[-1].get_file()
        photo_bytes = await photo.download_as_bytearray()

        input_image = Image.open(io.BytesIO(photo_bytes)).convert("RGBA")
        output_image = remove(input_image)

        bio = io.BytesIO()
        output_image.save(bio, format='PNG')
        bio.seek(0)

        await update.message.reply_photo(photo=bio, caption="✅ Transparent image ready, bhai 🔥")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()
