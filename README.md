# XOR-Wizard
Этот проект представляет собой Telegram-бота, который позволяет шифровать и расшифровывать текст с использованием алгоритма XOR. Бот предоставляет интерактивный интерфейс для работы с текстом и ключами, а также поддерживает генерацию случайных ключей. Проект был разработан в рамках курсовой работы и демонстрирует применение криптографических методов (XOR-шифрование) в реальном приложении.

## Основные функции

- **Шифрование текста**: Пользователь может ввести текст и ключ для шифрования. Бот возвращает зашифрованный текст в формате Base64 и его бинарное представление.
- **Дешифрование текста**: Пользователь может ввести зашифрованный текст и ключ для дешифрования. Бот возвращает исходный текст.
- **Генерация случайного ключа**: Бот может сгенерировать случайный ключ для шифрования.
- **Интерактивный интерфейс**: Бот использует кнопки и состояния для удобного взаимодействия с пользователем.

## Установка и запуск

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/ваш-username/название-репозитория.git
   ```

2. **Установите зависимости**:
   Убедитесь, что у вас установлен Python 3.8 или выше. Затем установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте бота**:
   - Создайте бота через [BotFather](https://core.telegram.org/bots#botfather) и получите токен.
   - Создайте файл `config.py` в корне проекта и добавьте туда токен:
     ```python
     TOKEN = 'ваш-токен-бота'
     ```

4. **Запустите бота**:
   ```bash
   python main.py
   ```

## Использование

1. **Запустите бота** в Telegram, нажав `/start`.
2. Выберите действие:
   - **🔐 Зашифровать текст**: Введите текст и ключ (или сгенерируйте случайный ключ).
   - **🔓 Расшифровать текст**: Введите зашифрованный текст и ключ.
3. Следуйте инструкциям бота.

## Пример работы

1. **Шифрование**:
   - Введите текст: `Привет, мир!`
   - Введите ключ: `ключ123`
   - Бот вернет зашифрованный текст в Base64 и его бинарное представление.

2. **Дешифрование**:
   - Введите зашифрованный текст: `8J+QjQ==`
   - Введите ключ: `ключ123`
   - Бот вернет исходный текст: `Привет, мир!`

## Технологии

- **Python 3.8+**
- **Aiogram** (библиотека для создания Telegram-ботов)
- **Base64** (кодирование и декодирование данных)
- **XOR-шифрование** (алгоритм шифрования)