from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from transcription.transcriber import transcribe

router = Router()

def is_text_message(message: Message) -> bool:
    return bool(message.text and not message.text.startswith('/'))

@router.message(is_text_message)
async def send_transcription(message: Message):
    try:
        transcription = transcribe(message.text)
        await message.reply(text=transcription)
    except Exception as e:
        # Логируем ошибку для отладки
        print(f"Error in transcription: {e}")
        await message.reply(text=LEXICON_RU['no_words_to_transcribe'])