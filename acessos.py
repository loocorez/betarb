import requests, json, math

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
def checknan(valor):
    vazio = False
    try:
        if math.isnan(valor): vazio = True
    except:
        try:
            if valor == None: vazio = True
        except:
            vazio = True
    finally:
        return vazio

def n_str(n_string):
    n_string.replace("'","''")
    n_string.replace('"', '""')
    return n_string
def insert_sports(self, nomex, slug, id, add_ind=False):
    if not slug in self.sports:
        if add_ind: self.mysql_conn.bd(f'INSERT IGNORE INTO ind_sports (sport_name, slug) VALUES ("{nomex}", "{slug}");', fetch=False)
        sqlgg = f'SELECT id from ind_sports WHERE sport_name="{nomex}";'
        check_ind = self.mysql_conn.bd(sqlgg, fetch=True)
        if check_ind:
            sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, id_ind_sport, slug) VALUES ({self.id_site},"{id}","{nomex}", {check_ind[0][0]},"{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
        else:
            sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, slug) VALUES ({self.id_site},"{id}","{nomex}", "{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
        id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
        id_ind = 0
        ativo = 1
        if id_bd == 0:
            t_id_bd = self.mysql_conn.bd(f'SELECT id, id_ind_sport, ativo FROM sit_sports WHERE id_site = {self.id_site} and id_site_sport = "{id}"', fetch=True)
            if t_id_bd:
                id_bd = t_id_bd[0][0]
                id_ind = t_id_bd[0][1]
                ativo = t_id_bd[0][2]
        else:
            t_id_ind = self.mysql_conn.bd(f'SELECT id_ind_sport FROM sit_sports WHERE id = {id_bd}', fetch=True)
            if t_id_ind:
                id_ind = t_id_ind[0][0]
        self.sports[slug] = {'name': nomex, 'slug': slug, 'id_bd': id_bd, 'id_site': id, 'id_ind': id_ind, 'ativo': ativo}

def insert_pais(self, nomex, slug, id, add_ind=False):
    if nomex == 'Eslováquia':
        print('')
    if not slug in self.paises:
        if add_ind: self.mysql_conn.bd(f'INSERT IGNORE INTO ind_paises (pais_name) VALUES ("{nomex}");', fetch=False)
        sqlgg = f'SELECT id from ind_paises WHERE pais_name="{nomex}";'
        check_ind = self.mysql_conn.bd(sqlgg, fetch=True)
        if check_ind:
            sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, id_ind_pais, slug) VALUES ({self.id_site},"{id}","{nomex}",{check_ind[0][0]},"{slug}") ON DUPLICATE KEY UPDATE site_pais_name="{nomex}", slug="{slug}";'
        else:
            sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, slug) VALUES ({self.id_site},"{id}","{nomex}","{slug}") ON DUPLICATE KEY UPDATE site_pais_name="{nomex}", slug="{slug}";'
        id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
        id_ind = 0
        if id_bd == 0:
            t_id_bd = self.mysql_conn.bd(f'SELECT id, id_ind_pais FROM sit_paises WHERE id_site = {self.id_site} and site_pais_name="{nomex}" and slug="{slug}"', fetch=True)
            if t_id_bd:
                id_bd = t_id_bd[0][0]
                id_ind = t_id_bd[0][1]
        else:
            t_id_ind = self.mysql_conn.bd(f'SELECT id_ind_pais FROM sit_paises WHERE id = {id_bd}', fetch=True)
            if t_id_ind:
                id_ind = t_id_ind[0][0]
        if id_bd == 0:
            print("")
        self.paises[slug] = {'name': nomex, 'id_bd': id_bd, 'id_site': id, 'id_ind': id_ind}

def insert_camp(self, nomex, slug, id, sport, pais, add_ind=False):
    sports = self.sports[sport]
    paises = self.paises[pais]
    if not slug in self.campeonatos and nomex != None:
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
        id_ind = 0
        if id_bd == 0:
            t_id_bd = self.mysql_conn.bd(f'SELECT id, id_ind_camp FROM sit_camp WHERE id_site = {self.id_site} and id_site_camp="{id}"', fetch=True)
            if t_id_bd:
                id_bd = t_id_bd[0][0]
                id_ind = t_id_bd[0][1]
        else:
            t_id_ind = self.mysql_conn.bd(f'SELECT id_ind_camp FROM sit_camp WHERE id = {id_bd}', fetch=True)
            if t_id_ind:
                id_ind = t_id_ind[0][0]
        self.campeonatos[slug] = {'name': nomex, 'id_bd': id_bd, 'id_site': id, 'id_ind': id_ind}

def insert_event(self, start_time, event_name, site_slug, site_id, site_status, sport, pais, camp, add_ind=False):
    camps = self.campeonatos[camp]
    sports = self.sports[sport]
    paises = self.paises[pais]
    if not site_id in self.eventos:
        sqlxx = f'INSERT INTO sit_events (id_ind_site, id_site_sport, id_site_pais, id_site_camp, start_time, event_name, site_slug, site_id, site_status) ' \
                f'VALUES ({self.id_site}, {sports["id_bd"]}, {paises["id_bd"]}, {camps["id_bd"]}, "{start_time}","{event_name}","{site_slug}", "{site_id}", {site_status}) ON DUPLICATE KEY ' \
                f'UPDATE start_time="{start_time}", event_name="{event_name}", site_slug="{site_slug}", site_status={site_status};'
        id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
        if id_bd == 0:
            t_id_bd = self.mysql_conn.bd(f'SELECT id FROM sit_events WHERE id_ind_site = {self.id_site} and site_id="{site_id}"', fetch=True)
            if t_id_bd:
                id_bd = t_id_bd[0][0]
        id_ind_events = 0
        if add_ind:
            sqlxx = f'INSERT IGNORE INTO ind_events (nome, start_time, id_ind_camp) VALUES ("{event_name}","{start_time}", {camps["id_ind"]});'
            id_ind_events = self.mysql_conn.bd(sqlxx, fetch=False)
            if id_ind_events == 0:
                t_id_ind_events = self.mysql_conn.bd(f'SELECT id FROM ind_events WHERE nome = "{event_name}" and id_ind_camp = {camps["id_ind"]}', fetch=True)
                if t_id_ind_events:
                    id_ind_events = t_id_ind_events[0][0]
            sqlxx = f'UPDATE sit_events SET id_ind_events={id_ind_events} WHERE id={id_bd};'
            self.mysql_conn.bd(sqlxx, fetch=False)
        # else:
        #     sqlxx = f'INSERT IGNORE INTO ind_events (id_ind_site, id_sit_events) VALUES ({self.id_site}, {id_bd});'
        #     id_ind_events = self.mysql_conn.bd(sqlxx, fetch=False)
        #     sqlxx = f'UPDATE sit_events SET id_ind_events={id_ind_events} WHERE id={id_bd};'
        self.eventos[site_id] = {'name': event_name, 'id_bd': id_bd, 'id_site': site_id, 'id_ind': id_ind_events, "start_time": start_time}

def insert_compet(self, sport, evento, site_id_compet, site_nome_compet, sit_tipo_compet, add_ind=False):
    sports = self.sports[sport]
    eventos = self.eventos[evento]
    if not (sport, site_id_compet) in self.competidores:
        sqlxx = f'INSERT INTO sit_compet (id_ind_site, id_site_sport, site_nome_compet, site_id_compet) ' \
                f'VALUES ({self.id_site}, {sports["id_bd"]}, "{site_nome_compet}", "{site_id_compet}") ON DUPLICATE KEY ' \
                f'UPDATE site_nome_compet="{site_nome_compet}";'
        id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
        if id_bd == 0:
            t_id_bd = self.mysql_conn.bd(f'SELECT id FROM sit_compet WHERE id_ind_site = {self.id_site} and site_id_compet="{site_id_compet}"', fetch=True)
            if t_id_bd: id_bd = t_id_bd[0][0]
        sqlxx = f'INSERT IGNORE INTO sit_events_compet (id_sit_event, id_sit_compet, tipo) VALUES ({eventos["id_bd"]}, {id_bd}, {sit_tipo_compet});'
        self.mysql_conn.bd(sqlxx, fetch=False)
        id_ind_compet = 0
        if add_ind and not checknan(sports['id_ind']) and sports['id_ind'] > 0: #
            sqlxx = f'INSERT IGNORE INTO ind_compet (id_ind_sport, nome) VALUES ({sports["id_ind"]}, "{site_nome_compet}");'
            id_ind_compet = self.mysql_conn.bd(sqlxx, fetch=False)
            if id_ind_compet == 0:
                t_id_ind_compet = self.mysql_conn.bd(f'SELECT id FROM ind_compet WHERE id_ind_sport = {sports["id_ind"]} and nome="{site_nome_compet}"', fetch=True)
                if t_id_ind_compet: id_ind_compet = t_id_ind_compet[0][0]
            sqlxx = f'INSERT IGNORE INTO ind_events_compet (id_ind_event, id_ind_compet, tipo) VALUES ({eventos["id_ind"]}, {id_ind_compet}, {sit_tipo_compet});'
            self.mysql_conn.bd(sqlxx, fetch=False)
            sqlxx = f'UPDATE sit_compet SET id_ind_compet={id_ind_compet} WHERE id={id_bd};'
            self.mysql_conn.bd(sqlxx, fetch=False)
        self.competidores[(sport, site_id_compet)] = {'name': site_nome_compet, 'id_bd': id_bd, 'id_site': site_id_compet, 'id_ind': id_ind_compet}

def insert_mercado(self, sport, site_id_market, site_nome_market, site_key, site_status_market, site_type_market, add_ind=False):
    if not (sport, site_id_market) in self.mercados:
        sports = self.sports[sport]
        sqlxx = f'INSERT INTO sit_mercados (id_site_sport, market_name, market_key, site_id_market, tipo, status) ' \
                f'VALUES ({sports["id_bd"]}, "{site_nome_market}", "{site_key}", "{site_id_market}", {site_type_market}, {site_status_market}) ON DUPLICATE KEY ' \
                f'UPDATE market_name="{site_nome_market}", market_key="{site_key}", tipo={site_type_market}, status={site_status_market};'
        id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
        ativo = 1
        if id_bd == 0:
            t_id_bd = self.mysql_conn.bd(f'SELECT id, ativo FROM sit_mercados WHERE id_site_sport = {sports["id_bd"]} and site_id_market="{site_id_market}"', fetch=True)
            if t_id_bd:
                id_bd = t_id_bd[0][0]
                ativo = t_id_bd[0][1]
        id_ind_mercado = 0
        if add_ind and not checknan(sports['id_ind']) and sports['id_ind'] > 0: #not checknan(sports['id_ind']) and
            sqlxx = f'INSERT IGNORE INTO ind_mercados (id_ind_sport, nome, tipo) VALUES ({sports["id_ind"]}, "{site_nome_market}", {site_type_market});'
            id_ind_mercado = self.mysql_conn.bd(sqlxx, fetch=False)
            if id_ind_mercado == 0:
                t_id_ind_mercado = self.mysql_conn.bd(f'SELECT id FROM ind_mercados WHERE id_ind_sport = {sports["id_ind"]} and nome="{site_nome_market}"', fetch=True)
                if t_id_ind_mercado: id_ind_mercado = t_id_ind_mercado[0][0]
            sqlxx = f'UPDATE sit_mercados SET id_ind_mercado={id_ind_mercado} WHERE id={id_bd};'
            self.mysql_conn.bd(sqlxx, fetch=False)
        self.mercados[(sport, site_id_market)] = {'name': site_nome_market, 'market_key': site_key, 'id_bd': id_bd, 'id_site': site_id_market, 'id_ind': id_ind_mercado, 'ativo': ativo, 'selecoes': {}}

def insert_selecao(self, sport, site_id_market, site_nome_selecao, add_ind=False):
    mercados = self.mercados[(sport, site_id_market)]
    if not site_nome_selecao in mercados['selecoes']:
        sqlxx = f'INSERT INTO sit_selecoes (id_sit_mercado, selecao_nome) ' \
                f'VALUES ({mercados["id_bd"]}, "{site_nome_selecao}") ON DUPLICATE KEY ' \
                f'UPDATE selecao_nome="{site_nome_selecao}";'
        id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
        if id_bd == 0:
            t_id_bd = self.mysql_conn.bd(f'SELECT id FROM sit_selecoes WHERE id_sit_mercado = {mercados["id_bd"]} and selecao_nome="{site_nome_selecao}"', fetch=True)
            if t_id_bd: id_bd = t_id_bd[0][0]
        id_ind_selecao = 0
        if add_ind and not checknan(mercados['id_ind']) and mercados['id_ind'] > 0:  #
            sqlxx = f'INSERT IGNORE INTO ind_selecoes (id_ind_mercado, nome) VALUES ({mercados["id_ind"]}, "{site_nome_selecao}");'
            id_ind_selecao = self.mysql_conn.bd(sqlxx, fetch=False)
            if id_ind_selecao == 0:
                t_id_ind_selecao = self.mysql_conn.bd(
                    f'SELECT id FROM ind_mercados WHERE id_ind_sport = {mercados["id_ind"]} and nome="{site_nome_selecao}"', fetch=True)
                if t_id_ind_selecao: id_ind_selecao = t_id_ind_selecao[0][0]
            sqlxx = f'UPDATE sit_selecoes SET id_ind_selecao={id_ind_selecao} WHERE id={id_bd};'
            self.mysql_conn.bd(sqlxx, fetch=False)
        self.mercados[(sport, site_id_market)]['selecoes'][site_nome_selecao] = {'name': site_nome_selecao,  'id_bd': id_bd, 'id_ind': id_ind_selecao} #'name2': site_nome_selecao2,
def insert_update_odd(self, id_sit_evento, id_sit_selecao, odd):
    sqlxx = f'INSERT INTO sit_events_odds (id_sit_evento, id_sit_selecao, odd) ' \
            f'VALUES ({id_sit_evento}, "{id_sit_selecao}", "{odd}") ON DUPLICATE KEY ' \
            f'UPDATE odd="{odd}";'
    id_bd = self.mysql_conn.bd(sqlxx, fetch=False)