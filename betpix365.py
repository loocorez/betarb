import requests, json
from concurrent.futures import ThreadPoolExecutor
from acessos import *


class c_betpix365:
    def __init__(self, conexao):
        self.id_site = 1
        self.all_campeonatos = {}
        self.conexao = conexao

    def get_all_campeonatos(self):
        url = 'https://betpix365.com/api-v2/left-menu/d/23/betpix365/eyJyZXF1ZXN0Qm9keSI6e319'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
                   'Referer': 'https://betpix365.com/ptb/bet/main',
                   'Accept': 'application/json, text/plain, */*',
                   'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Content-Type': 'application/json',
                   'Origin': 'https://betpix365.com',
                   'Sec-Fetch-Dest': 'empty',
                   'Sec-Fetch-Mode': 'cors',
                   'Sec-Fetch-Site': 'same-origin',
                   'encodedbody': 'eyJyZXF1ZXN0Qm9keSI6e319',
                   'languageid': '23',
                   'device': 'm',
                   'customorigin': 'https://betpix365.com',
                   'bragiurl': 'https://bragi.sportingtech.com/'
                   }
        data = get_url(url=url, headers=headers)

        sql_string = ''

        _sports = {}
        _paises = {}
        _campeonatos = {}
        with ThreadPoolExecutor(30) as executor:
            for esporte in data['data']:
                if not esporte['stN'] in esporte:
                    self.conexao.bd(f'INSERT IGNORE INTO ind_sports (sport_name) VALUES ("{esporte["stN"]}");', fetch=False)
                    sql = f'SELECT id FROM ind_sports WHERE sport_name = "{esporte["stN"]}";'
                    _sports[esporte['stN']] = self.conexao.bd(sql, fetch=True)[0][0]
                    #sqlxx = f'INSERT IGNORE INTO sit_sports (id_site, id_site_sport, site_sport_name, id_ind_sport) VALUES ({self.id_site},"{esporte["xid"]}","{esporte["stN"]}",{_sports[esporte["stN"]]});'
                    sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, id_ind_sport) VALUES ({self.id_site},"{esporte["xid"]}","{esporte["stN"]}",{_sports[esporte["stN"]]}) ON DUPLICATE KEY UPDATE site_sport_name="{esporte["stN"]}";'
                    self.conexao.bd(sqlxx, fetch=False)

                if not esporte['xid'] in self.all_campeonatos:
                    self.all_campeonatos[esporte['xid']] = {'esporte': esporte['stN'],
                                                      'stSURL': esporte['stSURL'],
                                                      'paises': {}}
                for pais in esporte['cs']:
                    if not pais['cN'] in _paises:
                        self.conexao.bd(f'INSERT IGNORE INTO ind_paises (pais_name) VALUES ("{pais["cN"]}");', fetch=False)
                        _paises[pais['cN']] = self.conexao.bd(f'SELECT id FROM ind_paises WHERE pais_name = "{pais["cN"]}";', fetch=True)[0][0]
                        sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, id_ind_pais) VALUES ({self.id_site},"{pais["xid"]}","{pais["cN"]}",{_paises[pais["cN"]]}) ON DUPLICATE KEY UPDATE site_pais_name="{pais["cN"]}";'
                        self.conexao.bd(sqlxx, fetch=False)
                    if not pais['xid'] in self.all_campeonatos[esporte['xid']]['paises']:
                        self.all_campeonatos[esporte['xid']]['paises'][pais['xid']] = {'nome': pais['cN'],
                                                                                        'cSURL': pais['cSURL'],
                                                                                        'camp': {}}
                    for camp in pais['sns']:
                        if not camp['lName'] in _campeonatos:
                            sql = f'INSERT IGNORE INTO ind_camp (id_ind_sport, id_ind_pais, camp_name) VALUES ({_sports[esporte["stN"]]},{_paises[pais["cN"]]},"{camp["seaN"]}");'
                            self.conexao.bd(sql, fetch=False)
                            _campeonatos[camp["seaN"]] = self.conexao.bd(f'SELECT id FROM ind_camp WHERE camp_name = "{camp["seaN"]}" and id_ind_pais = {_paises[pais["cN"]]} and id_ind_sport = {_sports[esporte["stN"]]};', fetch=True)[0][0]
                            sqlxx = f'INSERT INTO sit_camp (id_site, id_site_camp, site_camp_name, id_ind_camp) VALUES ({self.id_site},"{camp["sId"]}","{camp["seaN"]}",{_campeonatos[camp["seaN"]]}) ON DUPLICATE KEY UPDATE site_camp_name="{camp["seaN"]}";'
                            self.conexao.bd(sqlxx, fetch=False)

                        # if not [pais['cN']] in paises:
                        #     paises.append(pais['cN'])
                        if not camp['lId'] in self.all_campeonatos[esporte['xid']]['paises'][pais['xid']]['camp']:
                            self.all_campeonatos[esporte['xid']]['paises'][pais['xid']]['camp'][camp['lId']] = {'nome': camp['lName'],
                                                                                                                'seaSURL': camp['seaSURL'],
                                                                                                                'eventos': {}}
                        #temp_id = f"{esporte['stSURL']}/{pais['cSURL']}/{camp['seaSURL']}"
                        #self.all_campeonatos[esporte['xid']]['paises'][pais['xid']]['camp'][camp['lId']]['eventos'] = executor.submit(self.get_lista_eventos, temp_id)
                xxx = 0
            executor.shutdown(wait=True)
            #values = ','.join(f"('{key}',{hist[key][0]},{hist[key][1]})" for key in hist)
            # values_sports = ','.join(f"('{str(e)}')" for e in sports)
            # sql_sports = f"INSERT IGNORE INTO sit_sports (id_site, id_site_sport, site_sport_name) VALUES (" + values + ");"
            # self.conexao.bd(sql_string, fetch=False)
            for e in self.all_campeonatos:
                for p in self.all_campeonatos[e]['paises']:
                    for c in self.all_campeonatos[e]['paises'][p]['camp']:
                        self.all_campeonatos[e]['paises'][p]['camp'][c]['eventos'] = self.all_campeonatos[e]['paises'][p]['camp'][c]['eventos'].result()
                        y = 0

    def get_lista_eventos(self, id:str):
        url = f'https://betpix365.com/api-v2/fixture/category-details/d/23/betpix365/null/false/no-ante/20/{id}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
                    'Referer': f'https://betpix365.com/ptb/bet/fixture-detail/{id}',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'bragiurl': 'https://bragi.sportingtech.com/',
                    'Content-Type': 'application/json',
                    'Origin': 'https://betpix365.com',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin'}
        input_data = {'requestBody':{'betTypeGroupLimit':20,'bragiUrl':'https://bragi.sportingtech.com/'},'device':'d','languageId':23}
        response = post_url(url, headers, input_data)
        print('GET', url)
        _eventos = {}
        for data in response['data']:
            for cs in data['cs']:
                for sns in cs['sns']:
                    for fs in sns['fs']:
                        if not fs['fId'] in _eventos:
                            _eventos[fs['fId']] = fs
        return(_eventos)

    def get_event(self, id: int):
        data = {"requestBody": {"fixtureIds": [id], "bragiUrl": "https://bragi.sportingtech.com/"}, "device": "d", "languageId": 23}
        url = f"https://betpix365.com/api-v2/fixture-detail/d/23/betpix365/{id}"
        return(post_url(url, data))

    def teste(self):
        url = "https://sportsbet.io/graphql"
        data = {"operationName":"MainMarketsQuery","variables":{"language":"pt","site":"sportsbet","eventId":"RXZlbnQ6NjMzOGFhYjFmMzBmYjk0NjE5ZTlhNWM4"},"query":"query MainMarketsQuery($eventId: GraphqlId!, $language: String!) {\n  sportsbetNewGraphql {\n    id\n    getEventById(id: $eventId) {\n      id\n      type\n      name(language: \"en\")\n      sport {\n        id\n        name(language: \"en\")\n        __typename\n      }\n      tournament {\n        id\n        name(language: \"en\")\n        __typename\n      }\n      competitors {\n        name\n        id\n        __typename\n      }\n      mainMarkets {\n        ...MainEventMarketFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MainEventMarketFragment on SportsbetNewGraphqlMarket {\n  id\n  __typename\n  name(language: $language)\n  englishName: name(language: \"en\")\n  enName: name(language: \"en\")\n  status\n  selections {\n    ...ListEventMarketSelectionFragment\n    __typename\n  }\n  market_type {\n    id\n    __typename\n    name\n    description\n    translation_key\n    type\n    settings {\n      id\n      betBoostMultiplier\n      __typename\n    }\n  }\n  specifiers\n}\n\nfragment ListEventMarketSelectionFragment on SportsbetNewGraphqlMarketSelection {\n  id\n  __typename\n  name(language: $language)\n  enName: name(language: \"en\")\n  active\n  odds\n  probabilities\n  providerProductId\n  __typename\n}\n"}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Accept': '*/*',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://sportsbet.io/pt/sports/event/soccer/spain/la-liga/rayo-vallecano-v-cf-getafe-6338aab1f30fb94619e9a5c8',
            'content-type': 'application/json',
            'Origin': 'https://sportsbet.io',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cookie': 'cf_clearance=NlxFu4qAlWRNI184piZU8lp3mWeZsn6QicKct6auQZ4-1665705759-0-150; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; _sp_srt_id.b17c=32c3e070-6bae-4713-98e6-9e7f6539d7d6.1665694911.2.1665705765.1665696991.338d46dd-6a39-44ac-b97d-e7e97505ddf6; _wingify_pc_uuid=de100dd0ac4145e08977f201d9bda149; __tid=uid-7786973412.8842922656; _ga_SEKFV66B0S=GS1.1.1665705753.2.1.1665705764.49.0.0; _ga=GA1.2.1810921942.1665694912; tryMetamaskHide=true; adformfrpid=3498136337046941869; fs_uid=#BN5B8#5845328798126080:6645563275317248:::#/1697230917; fs_cid=1.0; _gid=GA1.2.653885333.1665694939; wingify_donot_track_actions=0; g_state={"i_p":1665702364505,"i_l":1}; GW_CLIENT_ID=11b1639507c8aee0fbd5f503020b1ec2cdc731bf97b8f19f3c5719f83a7cdae8; __cf_bm=XJHJRRTgUB_WIiistICdcdm22dbK_gOoERS0qyO4zSE-1665705763-0-AWaBS0Y83geasfFmyrvXFJxLf2gCaH/vfqcCrq8jvL2Jhxdgq48rmvpxIrOnyde+d67Kx9BNg0U5OcViI9VB+ffVR5fFidLMEFzKHgw5OGKkh/57gaAOFzLLtnrmoQAjUgJlVCBkjVxknHGjRWTIjx2d9Zs4B22zqkVPlrpcd9X0; cf_chl_2=a32c2d08843cb4b; cf_chl_prog=x13; MKTSRC={"t":1665705762425,"d":{"src":"direct","mdm":"direct","cmp":"direct","kwd":"","cnt":"","gc":"","msc":""}}; _dd_s=rum=1&id=0cc7fbce-dc4b-41a8-9938-94e1b97053f1&created=1665705762657&expire=1665706664952&logs=1; _sp_srt_ses.b17c=*; _gat_gtag_UA_31178637_53=1; _gat_UA-31178637-53=1; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzQ4N2NiYzU0ZmExYzgyZjBiNGMxNGQ='
        }
        xxx = post_url(url, headers,data)
        return xxx
