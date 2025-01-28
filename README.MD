# Audio Classification API

## Описание

Этот проект представляет собой API для загрузки и классификации аудиофайлов с использованием Google Cloud Speech-to-Text. Аудиофайлы передаются в формате OGG (кодек Opus), и API возвращает расшифровку речи или классификацию как "non-speech". Кроме того, в проекте реализована возможность преобразования текста в речь с использованием Google Text-to-Speech (gTTS).

---

## Требования

- Python 3.7+
- Установленные зависимости (см. ниже)
- Аккаунт Google Cloud с активированным Speech-to-Text API
- JSON-файл с ключом учетной записи службы Google Cloud

---

## Установка и запуск

### 1. Склонировать репозиторий
```bash
git clone https://github.com/ваш-репозиторий.git
cd ваш-репозиторий
```

### 2. Установить зависимости
```bash
pip install -r requirements.txt
```

### 3. Настроить переменные окружения
Создайте файл `.env` в корневой директории проекта и добавьте в него:
```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service_account_key.json
```
Убедитесь, что путь ведёт к вашему ключу учетной записи службы Google.

### 4. Запустить сервер
```bash
uvicorn second:app --reload
```

Сервер будет доступен по адресу `http://127.0.0.1:8000`.

---

## Использование

### Эндпоинты

#### 1. Проверка статуса
**GET** `/`
Возвращает сообщение о том, что API работает:
```json
{
  "message": "Audio Classification API is running"
}
```

#### 2. Загрузка и классификация аудиофайла
**POST** `/upload/`

**Параметры:**
- `file` (обязательный): Аудиофайл в формате OGG (кодек Opus)
- `language_code` (необязательный): Код языка аудио, по умолчанию "en-US"

**Пример запроса (cURL):**
```bash
curl -X POST "http://127.0.0.1:8000/upload/"      -F "file=@path_to_audio.ogg"      -F "language_code=ru-RU"
```

**Пример ответа (успешный):**
```json
{
  "status": "success",
  "data": {
    "classification": "speech",
    "transcription": "Пример текста из аудио"
  }
}
```

**Пример ответа (если речь не распознана):**
```json
{
  "status": "success",
  "data": {
    "classification": "non-speech",
    "confidence": 0.0
  }
}
```

**Пример ответа (ошибка):**
```json
{
  "status": "error",
  "message": "Описание ошибки"
}
```

---

### Использование Text-to-Speech

Для преобразования текста в речь используется скрипт `main.py`.

**Пример использования:**
```bash
python main.py
```

После запуска вы можете ввести текст, который будет преобразован в аудио и воспроизведён. Пример:
```
Введите текст для озвучивания: Привет, как дела?
```

Аудиофайл будет воспроизведён и удалён после воспроизведения.

---

## Особенности реализации

1. **Работа с Google Speech-to-Text API:**
   - Аудиофайлы передаются в формате OGG Opus.
   - Частота дискретизации файла должна соответствовать его реальным параметрам (например, 48,000 Гц).

2. **Локальное сохранение файлов:**
   - Все загруженные файлы сохраняются в директорию `uploaded_audio/`.

3. **Поддержка русского языка:**
   - Вы можете передавать параметр `language_code=ru-RU` для распознавания русской речи.

4. **Логирование:**
   - Все запросы и ответы от Google API логируются в консоли для упрощения отладки.

5. **Text-to-Speech:**
   - Скрипт использует библиотеку `gTTS` для преобразования текста в речь и воспроизведения аудио.

---

## Технические детали

- **Конфигурация Google Speech-to-Text:**
  ```python
  config = speech.RecognitionConfig(
      encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
      sample_rate_hertz=48000,
      language_code=language_code,
      alternative_language_codes=["ru-RU"],
      enable_automatic_punctuation=True
  )
  ```

- **Асинхронная обработка файлов:**
  Файлы сохраняются на сервер асинхронно с использованием `aiofiles`.

- **Text-to-Speech:**
  ```python
  tts = TextToSpeech(lang='ru')
  tts.synthesize_and_play("Привет, как дела?")
  ```

---

## Зависимости

Файл `requirements.txt` включает:
```
fastapi
google-cloud-speech
python-dotenv
uvicorn
aiofiles
gtts
playsound
```

Установите зависимости командой:
```bash
pip install -r requirements.txt
```

---

## Лицензия

Этот проект распространяется под [MIT License](LICENSE).

---
