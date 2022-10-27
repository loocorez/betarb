from betpix365 import c_betpix365
from sportsbet import c_sportsbet
from stake import c_stake
import time, json
from bd import class_bd
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
conexao = class_bd()
def teste1():
    # Vairables
    PATH = "C:\ETH\pythonProjectBet365\chromedriver.exe"
    WEBPAGE = "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php"#"https://sportsbet.io/"
    driver = webdriver.Chrome(PATH)
    driver.get(WEBPAGE)

#teste1()

def stake():
    v_stake = c_stake(conexao)

def sportsbet():
    v_sportsbet = c_sportsbet(conexao)
    v_sportsbet.get_data()
def betpix365():
    v_betpix365 = c_betpix365(conexao)
    # v_betpix365.get_dados()
    down=True
    print("Carregando eventos betpix365")
    if down:
        with open("rotas.json", "w") as outfile:
            json.dump(v_betpix365.all_campeonatos, outfile)
        print("Final  %.4f sec" % (time.time() - start_time))
    else:
        with open("rotas.json") as json_file:
            v_betpix365.all_campeonatos = json.load(json_file)

t = Thread(target=sportsbet, )
t.start()
t.join()


while True:
    time.sleep(1)
start_time = time.time()
