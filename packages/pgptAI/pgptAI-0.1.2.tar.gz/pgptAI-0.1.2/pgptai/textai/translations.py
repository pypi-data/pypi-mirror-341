import requests
from pgptai import textai


def create(model: str, language: list, text: str):

    if textai.api_base == "":
        textai.api_base = "https://ai.pgpt.cloud"

    url = f"{textai.api_base}/v1/translate/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {textai.api_key}",
    }
    data = {
        "to_lang": language,
        "text": text,
    }
    return requests.post(url, headers=headers, json=data).json()


def list():
    """
    该函数用于获取支持的语言列表
    """

    url = f"{textai.api_base}/v1/language/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {textai.api_key}",
    }
    return requests.post(url, headers=headers).json()
