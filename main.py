from betpix365 import c_betpix365
from sportsbet import c_sportsbet
import time, json
from bd import class_bd
conexao = class_bd()


url = "https://sportsbet.io/"


v_betpix365 = c_betpix365(conexao)
v_sportsbet = c_sportsbet(conexao)

#v_betpix365.get_dados()
v_sportsbet.get_dados()
start_time = time.time()
down=True
print("Carregando eventos betpix365")
if down:

    with open("rotas.json", "w") as outfile:
        json.dump(v_betpix365.all_campeonatos, outfile)
    print("Final  %.4f sec" % (time.time() - start_time))
else:
    with open("rotas.json") as json_file:
        v_betpix365.all_campeonatos = json.load(json_file)

xxx = 0
eventos_live = {}


