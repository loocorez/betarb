from betpix365 import betpix365
import time, json
from bd import class_bd

conexao = class_bd()

v_betpix365 = betpix365(conexao)

#testexxx = v_betpix365.teste()
start_time = time.time()
down=True
print("Carregando eventos betpix365")
if down:
    v_betpix365.get_all_campeonatos()
    with open("rotas.json", "w") as outfile:
        json.dump(v_betpix365.all_campeonatos, outfile)
    print("Final  %.4f sec" % (time.time() - start_time))
else:
    with open("rotas.json") as json_file:
        v_betpix365.all_campeonatos = json.load(json_file)

xxx = 0
eventos_live = {}


