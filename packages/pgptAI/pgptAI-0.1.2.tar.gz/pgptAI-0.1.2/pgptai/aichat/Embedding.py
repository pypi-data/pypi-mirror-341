import requests
from pgptai import aichat
import os

"""
该模块主要用于处理不同类型的文件并获取其 embeddings 。
"""


def pdf(file_path: str):
    url = aichat.api_base + "/v1/embeddings/"
    headers = {
        'Authorization': aichat.api_key
    }
    payload = {'type': 'pdf'}
    files = [
        ('file', (os.path.basename(file_path), open(file_path, 'rb'), 'application/pdf'))
    ]

    return requests.request("POST", url, headers=headers, data=payload, files=files).json()


def txt(file_path: str):
    url = aichat.api_base + "/v1/embeddings/"
    headers = {
        'Authorization': aichat.api_key
    }
    payload = {'type': 'txt'}
    files = [
        ('file', (os.path.basename(file_path), open(file_path, 'rb'), 'application/plain'))
    ]
    return requests.request("POST", url, headers=headers, data=payload, files=files).json()


def plain(text: str):
    url = aichat.api_base + "/v1/embeddings/"
    headers = {
        'Authorization': aichat.api_key
    }
    payload = {'type': 'plain', 'text': text}
    return requests.request("POST", url, headers=headers, data=payload).json()


def excel(file_path: str):
    url = aichat.api_base + "/v1/embeddings/"
    headers = {
        'Authorization': aichat.api_key
    }
    payload = {'type': 'excel'}
    files = [('file', (os.path.basename(file_path), open(file_path, 'rb'),
                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))]
    return requests.request("POST", url, headers=headers, data=payload, files=files).json()


def web(url: str):
    url = aichat.api_base + "/v1/embeddings/"
    headers = {
        'Authorization': aichat.api_key
    }
    payload = {'type': 'url', 'text': url}
    return requests.request("POST", url, headers=headers, data=payload).json()


def word(file_path: str):
    url = aichat.api_base + "/v1/embeddings/"
    headers = {
        'Authorization': aichat.api_key
    }
    payload = {'type': 'word'}
    files = [
        ('file', (os.path.basename(file_path), open(
            file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'))
    ]
    return requests.request("POST", url, headers=headers, data=payload, files=files).json()
