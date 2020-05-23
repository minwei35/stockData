import requests


def get_proxy():
    return requests.get("http://192.168.10.46:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://192.168.10.46:5010/delete/?proxy={}".format(proxy))
