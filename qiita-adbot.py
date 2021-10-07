from selenium import webdriver
import chromedriver_binary
from os import system
import requests
from lxml import html
from time import sleep
import random

email = input('Qiitaのメールアドレス:')
password = input('Qiitaのパスワード:')
tags = {}

subject = open('subject.txt', 'r')
text = open('text.txt', 'r')

def getTags():
    print('タグを収集中....')
    response = requests.get('https://qiita.com/tags')
    tree = html.fromstring(response.content)
    tags = tree.xpath('//div[@class="TagList__item"]/a/text()')
    print(tags)
    return tags
def login():
    print('アカウントにログイン中...')
    s = requests.session()

    response = s.get('https://qiita.com/login')
    tree = html.fromstring(response.content)
    csrfToken = tree.xpath('//input[@name="authenticity_token"]/@value')
    if(type(csrfToken) == list):
        csrfToken = csrfToken[0]

    print(csrfToken)
    response = s.post('https://qiita.com/login', data={ "authenticity_token": csrfToken, "identity": email, "password": password, "commit": "Qiita にログイン" }, headers={ "accept-language": "ja,en-US;q=0.9,en;q=0.8" })
    print(response.status_code)
    if response.status_code != 302:
        print('ログインに失敗しました')
        exit()
    print("ログイン成功"+response.headers.get('set-cookie'))
    return response.headers.get('set-cookie')
def post (tags, session):
    t = []
    for i in range(5):
        tag = random.choice(tags)
        if tag in t:
            i = i - 1
        else:
            t.append(tag)
    print('タグを決定しました'+t)
    response = requests.post('https://qiita.com/graphql', headers={ "cookie": session, "origin": "https://qiita.com" })
    tree = html.fromstring(response.content)
    print('記事の投稿が完了しました')


if __name__ == '__main__':
    tags = getTags()
    session = login()
    
    #while True:
     #   post(tags, session)
      #  sleep(0.5)