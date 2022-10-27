import requests, json

def get_url_json(url: str, headers:json) -> json:
    return (requests.get(url=url, headers=headers).json())

def post_url_json(url: str, headers:json, data: json) -> json:
    response = requests.post(url=url, json=data, headers=headers)
    return response.json()

def get_url_str(self, url: str, headers:json) -> requests.Response:
    return self.sessao.get(url=url, headers=headers, allow_redirects=False) #verify='./FiddlerRoot.cer'

def post_url_str(self, url: str, headers:json, data: json) -> requests.Response:
    response = self.sessao.post(url=url, json=data, headers=headers)
    return response

def insert_sports(self, nomex, slug, id, add_ind=False):
    if add_ind: self.mysql_conn.bd(f'INSERT IGNORE INTO ind_sports (sport_name) VALUES ("{nomex}");', fetch=False)
    sqlgg = f'SELECT id from ind_sports WHERE sport_name="{nomex}";'
    check_ind = self.mysql_conn.bd(sqlgg, fetch=True)
    if check_ind:
        sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, id_ind_sport, slug) VALUES ({self.id_site},"{id}","{nomex}", {check_ind[0][0]},"{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
    else:
        sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, slug) VALUES ({self.id_site},"{id}","{nomex}", "{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
    id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
    if id_bd == 0:
        t_id_bd = self.mysql_conn.bd(f'SELECT id FROM sit_sports WHERE id_site = {self.id_site} and id_site_sport = "{id}"', fetch=True)
        if t_id_bd: id_bd = t_id_bd[0][0]
    self.sports[slug] = {'name': nomex, 'slug': slug, 'id_bd': id_bd, 'id_site': id}

def insert_pais(self, nomex, slug, id, add_ind=False):
    if add_ind: self.mysql_conn.bd(f'INSERT IGNORE INTO ind_paises (pais_name) VALUES ("{nomex}");', fetch=False)
    sqlgg = f'SELECT id from ind_paises WHERE pais_name="{nomex}";'
    check_ind = self.mysql_conn.bd(sqlgg, fetch=True)
    if check_ind:
        sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, id_ind_pais, slug) VALUES ({self.id_site},"{id}","{nomex}",{check_ind[0][0]},"{slug}") ON DUPLICATE KEY UPDATE site_pais_name="{nomex}", slug="{slug}";'
    else:
        sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, slug) VALUES ({self.id_site},"{id}","{nomex}","{slug}") ON DUPLICATE KEY UPDATE site_pais_name="{nomex}", slug="{slug}";'
    id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
    if id_bd == 0:
        t_id_bd = self.mysql_conn.bd(f'SELECT id FROM sit_paises WHERE id_site = {self.id_site} and id_site_pais="{id}"', fetch=True)
        if t_id_bd: id_bd = t_id_bd[0][0]
    self.paises[slug] = {'name': nomex, 'id_bd': id_bd, 'id_site': id}

def insert_camp(self, nomex, slug, id, sports, paises, add_ind=False):
    ind_camp = 0
    if add_ind:
        ind_sport = self.mysql_conn.bd(f'SELECT id FROM ind_sports WHERE sport_name = "{sports["name"]}";', fetch=True)[0][0] #_sports[esporte["stSURL"]]
        ind_pais = self.mysql_conn.bd(f'SELECT id FROM ind_paises WHERE pais_name = "{paises["name"]}";', fetch=True)[0][0] #_paises[pais["cSURL"]]
        if ind_pais != 0 and ind_sport != 0:
            self.mysql_conn.bd(f'INSERT IGNORE INTO ind_camp (id_ind_sport, id_ind_pais, camp_name) VALUES ({ind_sport},{ind_pais},"{nomex}");', fetch=False)
            ind_camp = self.mysql_conn.bd(f'SELECT id FROM ind_camp WHERE camp_name = "{nomex}" and id_ind_pais = {ind_pais} and id_ind_sport = {ind_sport};', fetch=True)[0][0]
    # self.campeonatos[camp["seaSURL"]] = {'name': camp["seaN"].strip(), 'id': camp["sId"]}
    # sqlxx = f'INSERT INTO sit_camp (id_site, id_site_camp, site_camp_name, id_ind_camp, slug) VALUES ({self.id_site},"{camp["sId"]}","{camp["seaN"].strip()}",{_campeonatos[camp["seaSURL"]]},"{camp["seaSURL"]}") ON DUPLICATE KEY UPDATE site_camp_name="{camp["seaN"].strip()}", slug="{camp["seaSURL"]}";'
    # self.mysql_conn.bd(sqlxx, fetch=False)
    if ind_camp != 0:
        sqlxx = f'INSERT INTO sit_camp (id_site, id_site_sport, id_site_pais, id_site_camp, site_camp_name, id_ind_camp, slug) VALUES ({self.id_site}, {sports["id_bd"]}, {paises["id_bd"]}, "{id}","{nomex}",{ind_camp},"{slug}") ON DUPLICATE KEY UPDATE site_camp_name="{nomex}", slug="{slug}";'
    else:
        sqlxx = f'INSERT INTO sit_camp (id_site, id_site_sport, id_site_pais, id_site_camp, site_camp_name, slug) VALUES ({self.id_site}, {sports["id_bd"]}, {paises["id_bd"]}, "{id}","{nomex}","{slug}") ON DUPLICATE KEY UPDATE site_camp_name="{nomex}", slug="{slug}";'
    id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
    if id_bd == 0:
        t_id_bd = self.mysql_conn.bd(f'SELECT id FROM sit_camp WHERE id_site = {self.id_site} and id_site_camp="{id}"', fetch=True)
        if t_id_bd: id_bd = t_id_bd[0][0]
    self.campeonatos[slug] = {'name': nomex, 'id_bd': id_bd, 'id_site': id}

def insert_event(self, start_time, event_name, site_slug, site_id, site_status, sports, paises, camps, add_ind=False):
    sqlxx = f'INSERT INTO sit_events (id_ind_site, id_site_sport, id_site_pais, id_site_camp, start_time, event_name, site_slug, site_id, site_status) ' \
            f'VALUES ({self.id_site}, {sports["id_bd"]}, {paises["id_bd"]}, {camps["id_bd"]}, "{start_time}","{event_name}","{site_slug}", "{site_id}", {site_status}) ON DUPLICATE KEY ' \
            f'UPDATE start_time="{start_time}", event_name="{event_name}", site_slug="{site_slug}", site_status={site_status};'
    id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
    if id_bd == 0:
        t_id_bd = self.mysql_conn.bd(f'SELECT id FROM sit_events WHERE id_ind_site = {self.id_site} and site_id="{site_id}"', fetch=True)
        if t_id_bd: id_bd = t_id_bd[0][0]
    self.eventos[site_id] = {'name': event_name, 'id_bd': id_bd, 'id_site': site_id, "start_time": start_time}
    if add_ind:
        sqlxx = f'INSERT IGNORE INTO ind_events (id_ind_site, id_sit_events) VALUES ({self.id_site}, {id_bd});'
        id_ind_events = self.mysql_conn.bd(sqlxx, fetch=False)
        if id_ind_events == 0:
            t_id_ind_events = self.mysql_conn.bd(f'SELECT id FROM ind_events WHERE id_ind_site = {self.id_site} and id_sit_events="{id_bd}"', fetch=True)
            if t_id_ind_events: id_ind_events = t_id_ind_events[0][0]
        sqlxx = f'UPDATE sit_events SET id_ind_events={id_ind_events} WHERE id={id_bd};'
        self.mysql_conn.bd(sqlxx, fetch=False)

def insert_compet(self, sports, site_id_compet, site_nome_compet, add_ind=False):
    sqlxx = f'INSERT INTO sit_compet (id_ind_site, id_site_sport, site_nome_compet, site_id_compet, id_ind_compet) ' \
            f'VALUES ({self.id_site}, {sports["id_bd"]}, "{site_nome_compet}", "{site_id_compet}") ON DUPLICATE KEY ' \
            f'UPDATE site_nome_compet="{site_nome_compet}";'
    id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
    if id_bd == 0:
        t_id_bd = self.mysql_conn.bd(f'SELECT id FROM sit_events WHERE id_ind_site = {self.id_site} and site_id="{site_id_compet}"', fetch=True)
        if t_id_bd: id_bd = t_id_bd[0][0]
    self.compet[(sports['id_bd'], site_id_compet)] = {'name': site_nome_compet, 'id_bd': id_bd, 'id_site': site_id_compet}
    if add_ind:
        sqlxx = f'INSERT IGNORE INTO ind_compet (id_ind_sport, nome) VALUES ({self.id_site}, {id_bd});'
        id_ind_events = self.mysql_conn.bd(sqlxx, fetch=False)
        if id_ind_events == 0:
            t_id_ind_events = self.mysql_conn.bd(f'SELECT id FROM ind_events WHERE id_ind_site = {self.id_site} and id_sit_events="{id_bd}"', fetch=True)
            if t_id_ind_events: id_ind_events = t_id_ind_events[0][0]
        sqlxx = f'UPDATE sit_events SET id_ind_events={id_ind_events} WHERE id={id_bd};'
        self.mysql_conn.bd(sqlxx, fetch=False)
