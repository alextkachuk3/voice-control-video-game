import json
import os.path


class Translator:
    __registered_languages = {}
    __language = {}
    __title = None

    @staticmethod
    def change_language(title:str):
        if title not in Translator.__registered_languages:
            raise KeyError(f"Language {title} is not registered")

        Translator.__title = title
        Translator.__language = Translator.__registered_languages[title]

    @staticmethod
    def register_language(title:str, filename:str, encoding=None):
        if not os.path.exists(filename):
            raise AttributeError(f"File {filename} does not exist")

        if title in Translator.__registered_languages:
            return

        file = open(filename, "r", encoding=encoding)
        text = file.read()
        file.close()

        language = json.loads(text)
        Translator.__registered_languages[title] = language

        if Translator.__title is None:
            Translator.__title = title
            Translator.__language = Translator.__registered_languages[title]

    @staticmethod
    def translate(key:str):
        if key in Translator.__language:
            return Translator.__language[key]

        return key

    @staticmethod
    def tr(key:str):
        return Translator.translate(key)

    @staticmethod
    def get_language_list():
        return Translator.__registered_languages.keys()


def tr(key:str|tuple[str]|list[str]):
    if isinstance(key, tuple) or isinstance(key, list):
        return [Translator.tr(value) for value in key]
    return Translator.tr(key)
