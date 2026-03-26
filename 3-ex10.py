import pytest

def test_phrase_length():
    phrase = input("Введите фразу: ")

    assert len(phrase) < 15, f"Ошибка: фраза содержит {len(phrase)} символов, количество символов не должно превышать 15"