from pgptai import audioai
import requests


def create(model: str, voice: str, input: str):

    if audioai.api_base == "":
        audioai.api_base = "https://ai.pgpt.cloud"

    url = f'{audioai.api_base}/v1/speech/text2speech'
    headers = {
        'accept': 'application/json',
        "Authorization": f"Bearer {audioai.api_key}"
    }
    data = {
        'voice_name': voice,
        'text': input,
    }
    return requests.post(url, headers=headers, json=data).json()


def list():
    """
    该函数用于获取支持的语言列表
    """
    url = f'{audioai.api_base}/v1/speech/text2speech/voices'
    headers = {
        'accept': 'application/json',
        "Authorization": f"Bearer {audioai.api_key}"
    }
    return requests.request("POST", url, headers=headers).json()
