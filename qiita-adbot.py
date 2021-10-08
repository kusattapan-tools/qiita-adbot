from selenium import webdriver
import chromedriver_binary
from os import system
import requests
from lxml import html
from time import sleep
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading

combos = open('combos.txt', 'r').read().split('\n')
print(combos)
tags = {}

subject = "ポイ活の勧め。海外ポイントサイト・DropGCの紹介。"
text = """
皆さんはポイ活をしていますか？メディアで見たり聞いたりする機会もあると思います。

ポイ活とはポイント活動の略称です。ポイントを貯めれば、日々の生活をお得にできます。現金化する事も可能で、ポイントには夢が一杯あります！お小遣いが少しでも増えたら嬉しいですよね。

私自身はポイ活を2017年くらいからしています。決して怪しい活動ではないのでご安心を。

では、ポイ活はどうやって始められるのでしょうか。難しい手続きは一切ありません。ポイントサイトに登録するか、アプリを使うだけです。スマホやパソコンで簡単にお小遣い稼ぎができます。

私が登録しているポイントサイトをご紹介します。それは「DropGC」です。

大量広告で高還元の多いDropGC。10ポイント＝1円という特殊な設定から「実は大した金額じゃないのでは・・」と疑われて損しているように思います。同じ広告を比較すると平均的にモッピーやげん玉を上回っています。

DropGCの利用に慣れてきたら、注目したいのが友達紹介制度です。家族や知人、ブログやツイッターなどで紹介することができます。紹介するとポイントがついたり、利用してくれた案件の数十%がずっと還元されるシステムです。もちろん友達のポイントが減ることはありません。
とても魅力的なこの制度を生かしてみましょう。

広告量やゲーム量が多く、最も少額の100円から無料で交換できるので、とりあえず換金してみたいなら1番手軽にお小遣いにできます。
0歳以上から登録利用無料です。

どのサイトも登録や利用は無料なので、組み合わせて利用するのもオススメです。高報酬なポイントサイトが多いので、たくさん登録しすぎると使いきれない、ポイントが分散して稼ぎにくいと感じます。DropGC1本を極めるか、メインサイト＋比較サイトが少しあると便利です。

この業界の中では珍しく米国に本拠を置く財団が運営しています。
非常に安全性の高いサイトです

DropGCでは、全ページでSSL/TLSを導入しています。

SSL/TLSというのは、情報を暗号化して送受信することで第三者から大切な情報を勝手に見られないようにする技術です。

ちなみに、SSL/TLSの導入は、サイトURL「http」の後に「ｓ」があることで確認することができ、DropGCでもバッチリ確認できます。

全然稼げないポイントサイトも多いので、適当に選んでいるとまったく稼げないことが多いです。

しかし、DropGCはしっかり使えば、かなりの金額を稼ぐことも可能です。

https://dropgc.gift
【↑此方のリンクからDropGCに登録可能です】
"""


def getTags():
    print('タグを収集中....')
    response = requests.get('https://qiita.com/tags')
    tree = html.fromstring(response.content)
    tags = tree.xpath('//div[@class="TagList__item"]/a/text()')
    print(tags)
    return tags
def login(driver):
    print('アカウントにログイン中...')
    driver.get('https://qiita.com/login')

    cred = random.choice(combos)
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//input[@name="identity"]')))
    driver.find_element_by_xpath('//input[@name="identity"]').send_keys(cred)
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
    driver.find_element_by_xpath('//input[@name="password"]').send_keys(cred)
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//input[@name="commit"]')))
    driver.find_element_by_xpath('//input[@name="commit"]').click()
    return
def post (tags, driver):
    t = []
    for i in range(5):
        tag = random.choice(tags)
        if tag in t:
            i = i - 1
        else:
            t.append(tag)
    tagStr = ''
    for tagg in t:
        tagStr = tagStr + tagg + " "
    driver.execute_script('return location.href="https://qiita.com/drafts/new";')

    print('タグを決定しました'+tagStr)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@class="css-12fqrnh e1aqgsb41"]')))
    driver.find_element_by_xpath('//input[@class="css-12fqrnh e1aqgsb41"]').send_keys(subject)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//textarea[@class="css-avadu4"]')))
    driver.find_element_by_xpath('//textarea[@class="css-avadu4"]').send_keys(text)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@class="css-19fi7g8 ed5758y1"]')))
    driver.find_element_by_xpath('//input[@class="css-19fi7g8 ed5758y1"]').send_keys(tagStr)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[@class="e9bkwgs1 css-8voofm e1rb7ucl0"]')))
    driver.find_element_by_xpath('//button[@class="e9bkwgs1 css-8voofm e1rb7ucl0"]').click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[@class="css-lc87ok e1rb7ucl0"]')))
    if(len(driver.find_elements_by_xpath('//input[@class="css-15ro776"]')) > 0):
        for check in driver.find_elements_by_xpath('//input[@class="css-15ro776"]'):
            check.click()

    driver.find_element_by_xpath('//button[@class="css-lc87ok e1rb7ucl0"]').click()
    print('記事の投稿が完了しました')

def main ():
    driver = webdriver.Chrome()
    try:
        tags = getTags()
        login(driver)
    
        while True:
            try:
                post(tags, driver)
            except:
                login(driver)
            sleep(0.5)
    except:
        driver.quit()
        main()

if __name__ == '__main__':
    for i in range(5):
        threading.Thread(target=main).start()