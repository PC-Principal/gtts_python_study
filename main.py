from gtts import gTTS
from playsound import playsound
import os

class TextToSpeech:
    """
    Класс для преобразования текста в аудио и воспроизведения его.
    """

    def __init__(self, lang: str = 'ru') -> None:
        """
        Инициализирует объект TextToSpeech с указанным языком.

        :param lang: Код языка (по умолчанию 'ru' для русского).
        """
        self.lang = lang

    def synthesize_and_play(self, text: str) -> None:
        """
        Преобразует текст в аудио, сохраняет в файл, воспроизводит его и удаляет файл.

        :param text: Текст для синтеза речи.
        """
        if not text.strip():
            print("Пустой текст не может быть озвучен.")
            return

        try:
            # Создаём объект gTTS
            tts = gTTS(text=text, lang=self.lang)

            # Временное имя файла
            filename = "output.mp3"

            # Сохраняем аудио в файл
            tts.save(filename)
            print("Аудиофайл сохранён как 'output.mp3'")

            # Воспроизводим аудиофайл
            playsound(filename)

            # Удаляем файл после воспроизведения (опционально)
            os.remove(filename)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    user_text = input("Введите текст для озвучивания: ")
    tts = TextToSpeech(lang='ru')  # Инициализируем с языком по умолчанию (русский)
    tts.synthesize_and_play(user_text)