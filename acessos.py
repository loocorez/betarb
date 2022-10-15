import requests, json

def get_url_json(url: str, headers:json) -> json:
    return (requests.get(url=url, headers=headers).json())

def post_url_json(url: str, headers:json, data: json) -> json:
    response = requests.post(url=url, json=data, headers=headers)
    return response.json()

def get_url_str(url: str, headers:json) -> requests.Response:
    return requests.get(url=url, headers=headers) #verify='./FiddlerRoot.cer'

def post_url_str(url: str, headers:json, data: json) -> requests.Response:
    response = requests.post(url=url, json=data, headers=headers)
    return response

def insert_sports(self, nomex, slug, id, add_ind=False):
    if add_ind: self.conexao.bd(f'INSERT IGNORE INTO ind_sports (sport_name) VALUES ("{nomex}");', fetch=False)
    sqlgg = f'SELECT id from ind_sports WHERE sport_name="{nomex}";'
    check_ind = self.conexao.bd(sqlgg, fetch=True)
    if check_ind:
        sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, id_ind_sport, slug) VALUES ({self.id_site},"{id}","{nomex}", {check_ind[0][0]},"{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
    else:
        sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, slug) VALUES ({self.id_site},"{id}","{nomex}", "{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
    id_bd = self.conexao.bd(sqlxx, fetch=False)
    if id_bd == 0:
        t_id_bd = self.conexao.bd(f'SELECT id FROM sit_sports WHERE id_site = {self.id_site} and id_site_sport = "{id}"', fetch=True)
        if t_id_bd: id_bd = t_id_bd[0][0]
    self.sports[slug] = {'name': nomex, 'slug': slug, 'id_bd': id_bd, 'id_site': id}

def insert_pais(self, nomex, slug, id, add_ind=False):
    if add_ind: self.conexao.bd(f'INSERT IGNORE INTO ind_paises (pais_name) VALUES ("{nomex}");', fetch=False)
    sqlgg = f'SELECT id from ind_paises WHERE pais_name="{nomex}";'
    check_ind = self.conexao.bd(sqlgg, fetch=True)
    if check_ind:
        sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, id_ind_pais, slug) VALUES ({self.id_site},"{id}","{nomex}",{check_ind[0][0]},"{slug}") ON DUPLICATE KEY UPDATE site_pais_name="{nomex}", slug="{slug}";'
    else:
        sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, slug) VALUES ({self.id_site},"{id}","{nomex}","{slug}") ON DUPLICATE KEY UPDATE site_pais_name="{nomex}", slug="{slug}";'
    id_bd = self.conexao.bd(sqlxx, fetch=False)
    if id_bd == 0:
        t_id_bd = self.conexao.bd(f'SELECT id FROM sit_paises WHERE id_site = {self.id_site} and id_site_pais="{id}"', fetch=True)
        if t_id_bd: id_bd = t_id_bd[0][0]
    self.paises[slug] = {'name': nomex, 'id_bd': id_bd, 'id_site': id}

def insert_camp(self, nomex, slug, id, sports, paises, add_ind=False):
    ind_camp = 0
    if add_ind:
        ind_sport = self.conexao.bd(f'SELECT id FROM ind_sports WHERE sport_name = "{sports["name"]}";', fetch=True)[0][0] #_sports[esporte["stSURL"]]
        ind_pais = self.conexao.bd(f'SELECT id FROM ind_paises WHERE pais_name = "{paises["name"]}";', fetch=True)[0][0] #_paises[pais["cSURL"]]
        if ind_pais != 0 and ind_sport != 0:
            self.conexao.bd(f'INSERT IGNORE INTO ind_camp (id_ind_sport, id_ind_pais, camp_name) VALUES ({ind_sport},{ind_pais},"{nomex}");', fetch=False)
            ind_camp = self.conexao.bd(f'SELECT id FROM ind_camp WHERE camp_name = "{nomex}" and id_ind_pais = {ind_pais} and id_ind_sport = {ind_sport};', fetch=True)[0][0]
    # self.campeonatos[camp["seaSURL"]] = {'name': camp["seaN"].strip(), 'id': camp["sId"]}
    # sqlxx = f'INSERT INTO sit_camp (id_site, id_site_camp, site_camp_name, id_ind_camp, slug) VALUES ({self.id_site},"{camp["sId"]}","{camp["seaN"].strip()}",{_campeonatos[camp["seaSURL"]]},"{camp["seaSURL"]}") ON DUPLICATE KEY UPDATE site_camp_name="{camp["seaN"].strip()}", slug="{camp["seaSURL"]}";'
    # self.conexao.bd(sqlxx, fetch=False)
    if ind_camp != 0:
        sqlxx = f'INSERT INTO sit_camp (id_site, id_site_sport, id_site_pais, id_site_camp, site_camp_name, id_ind_camp, slug) VALUES ({self.id_site}, {sports["id_bd"]}, {paises["id_bd"]}, "{id}","{nomex}",{ind_camp},"{slug}") ON DUPLICATE KEY UPDATE site_camp_name="{nomex}", slug="{slug}";'
    else:
        sqlxx = f'INSERT INTO sit_camp (id_site, id_site_sport, id_site_pais, id_site_camp, site_camp_name, slug) VALUES ({self.id_site}, {sports["id_bd"]}, {paises["id_bd"]}, "{id}","{nomex}","{slug}") ON DUPLICATE KEY UPDATE site_camp_name="{nomex}", slug="{slug}";'
    id_bd = self.conexao.bd(sqlxx, fetch=False)
    if id_bd == 0:
        t_id_bd = self.conexao.bd(f'SELECT id FROM sit_camp WHERE id_site = {self.id_site} and id_site_camp="{id}"', fetch=True)
        if t_id_bd: id_bd = t_id_bd[0][0]
    self.campeonatos[slug] = {'name': nomex, 'id_bd': id_bd, 'id_site': id}

