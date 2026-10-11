"""Консольний англо-французький словник.

Слова зберігаються у файлі dictionary.json (слово англійською -> переклад французькою).
Можна додавати, видаляти, шукати й змінювати записи.
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dictionary.json")

DEFAULT_WORDS = {
    "hello": "bonjour",
    "goodbye": "au revoir",
    "thank you": "merci",
    "cat": "chat",
    "dog": "chien",
    "house": "maison",
    "book": "livre",
}


def load_words():
    """Читає словник із файлу; якщо файлу немає або він пошкоджений, повертає початковий набір."""
    if not os.path.exists(DATA_FILE):
        return dict(DEFAULT_WORDS)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
    except (json.JSONDecodeError, OSError):
        print("Не вдалося прочитати dictionary.json, використано початковий набір слів.")
    return dict(DEFAULT_WORDS)


def save_words(words):
    """Записує словник у файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2, sort_keys=True)


def find_key(words, word):
    """Шукає слово без урахування регістру; повертає ключ зі словника або None."""
    word = word.strip().lower()
    for key in words:
        if key.lower() == word:
            return key
    return None


def ask(prompt):
    """Запитує непорожній рядок."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Рядок не може бути порожнім.")


def add_word(words):
    english = ask("Слово англійською: ")
    if find_key(words, english):
        print(f"Слово «{english}» вже є у словнику. Скористайтеся пунктом «Змінити».")
        return
    french = ask("Переклад французькою: ")
    words[english] = french
    save_words(words)
    print(f"Додано: {english} -> {french}")


def delete_word(words):
    key = find_key(words, ask("Яке слово видалити: "))
    if key is None:
        print("Такого слова немає.")
        return
    del words[key]
    save_words(words)
    print(f"Видалено: {key}")


def search_word(words):
    query = ask("Що шукати (слово англійською або його частина, також можна французьке): ").lower()
    exact = find_key(words, query)
    if exact:
        print(f"{exact} -> {words[exact]}")
        return
    matches = {k: v for k, v in words.items() if query in k.lower() or query in v.lower()}
    if not matches:
        print("Нічого не знайдено.")
        return
    print("Схожі записи:")
    for k, v in sorted(matches.items()):
        print(f"  {k} -> {v}")


def edit_word(words):
    key = find_key(words, ask("Яке слово змінити: "))
    if key is None:
        print("Такого слова немає.")
        return
    print(f"Зараз: {key} -> {words[key]}")
    new_english = input("Нове слово англійською (Enter, щоб залишити): ").strip()
    new_french = input("Новий переклад французькою (Enter, щоб залишити): ").strip()
    if not new_english and not new_french:
        print("Нічого не змінено.")
        return
    translation = new_french or words[key]
    if new_english and new_english != key:
        other = find_key(words, new_english)
        if other is not None and other != key:
            print(f"Слово «{new_english}» вже є у словнику, зміну скасовано.")
            return
        del words[key]
        key = new_english
    words[key] = translation
    save_words(words)
    print(f"Збережено: {key} -> {translation}")


def show_all(words):
    if not words:
        print("Словник порожній.")
        return
    width = max(len(k) for k in words)
    for k in sorted(words, key=str.lower):
        print(f"  {k.ljust(width)} -> {words[k]}")
    print(f"Усього слів: {len(words)}")


MENU = """
=== Англо-французький словник ===
1. Додати слово
2. Видалити слово
3. Знайти слово
4. Змінити слово
5. Показати всі слова
0. Вихід
"""

ACTIONS = {
    "1": add_word,
    "2": delete_word,
    "3": search_word,
    "4": edit_word,
    "5": show_all,
}


def main():
    words = load_words()
    while True:
        print(MENU)
        choice = input("Ваш вибір: ").strip()
        if choice == "0":
            print("До побачення! Au revoir!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Невідомий пункт меню.")
            continue
        action(words)


if __name__ == "__main__":
    main()
