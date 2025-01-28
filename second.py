from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import aiofiles
import os
from google.cloud import speech
from typing import Dict, Any
from dotenv import load_dotenv

class AudioClassificationApp:
    def __init__(self):
        # Загрузка переменных окружения из .env файла
        load_dotenv()

        # Инициализация FastAPI приложения
        self.app = FastAPI()
        # Директория для сохранения загруженных файлов
        self.upload_dir = "uploaded_audio"
        # Создание директории, если она не существует
        os.makedirs(self.upload_dir, exist_ok=True)
        # Проверка наличия переменной окружения GOOGLE_APPLICATION_CREDENTIALS
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS not set in .env file")

        # Инициализация клиента Google Cloud Speech-to-Text
        self.speech_client = speech.SpeechClient()
        # Настройка маршрутов (эндпоинтов) приложения
        self.setup_routes()

    def setup_routes(self):
        """ Эндпоинт для загрузки аудиофайлов """
        @self.app.post("/upload/")
        async def upload_audio(
            file: UploadFile = File(...),
            language_code: str = Form(default="en-US")
        ) -> JSONResponse:
            # Вызов метода для обработки загрузки аудиофайлов
            return await self.upload_audio(file, language_code)

        # Эндпоинт для проверки статуса приложения
        @self.app.get("/")
        def root() -> Dict[str, str]:
            # Возврат сообщения о том, что приложение работает
            return self.root()

    async def upload_audio(self, file: UploadFile, language_code: str) -> JSONResponse:
        """Загрузка аудиофайла и отправка на классификацию"""
        # Формирование полного пути для сохранения файла
        original_file_path = os.path.join(self.upload_dir, file.filename)

        # Сохранение файла на сервер асинхронно
        async with aiofiles.open(original_file_path, 'wb') as out_file:
            # Чтение содержимого загруженного файла
            content = await file.read()
            # Запись содержимого в локальный файл
            await out_file.write(content)

        # Конвертация файла в байтовый формат для Google Speech-to-Text
        with open(original_file_path, 'rb') as audio_file:
            audio_content = audio_file.read()
        # Конфигурация для Google Speech-to-Text
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000, # Это важно, файл что сохраняется в директорию должен совпадать по диапазону иначе на спарсит в текст
            language_code=language_code,
            alternative_language_codes=["ru-RU"],
            enable_automatic_punctuation=True
        )

        try:
            # Отправка аудиофайла на распознавание речи
            response = self.speech_client.recognize(config=config, audio=audio)
            print(response)

            if response.results:
                # Если распознавание прошло успешно, анализируем результаты
                transcription = response.results[0].alternatives[0].transcript
                return JSONResponse(content={"status": "success", "data": {"classification": "speech", "transcription": transcription}})
            else:
                # Если текст не распознан, возможно это музыка или шум
                return JSONResponse(content={"status": "success", "data": {"classification": "non-speech", "confidence": 0.0}})

        except Exception as e:
            # Обработка ошибок API
            return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

    def root(self) -> Dict[str, str]:
        # Возвращает сообщение, подтверждающее работу API
        return {"message": "Audio Classification API is running"}

# Инициализация экземпляра приложения
app_instance = AudioClassificationApp()
# Экспорт FastAPI приложения для запуска
app = app_instance.app
