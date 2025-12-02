#!/usr/bin/env python
"""
Генератор секретного ключа для Django.
Использование: python generate_secret_key.py
"""

import secrets
import string


def generate_secret_key():
    # Генерируем случайный ключ длиной 50 символов
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Убираем проблемные символы
    alphabet = alphabet.replace("'", "").replace('"', '').replace('\\', '')

    secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))
    return secret_key


if __name__ == '__main__':
    key = generate_secret_key()
    print(f"Сгенерированный SECRET_KEY:")
    print(f"SECRET_KEY={key}")
    print("\nСкопируйте эту строку в ваш .env файл")