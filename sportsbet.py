from concurrent.futures import ThreadPoolExecutor
from acessos import *
from bs4 import BeautifulSoup
import codecs, html, json
import cloudscraper
class c_sportsbet:
    def __init__(self, conexao):
        self.id_site = 2
        self.conexao = conexao
        self.cookies = '_ga_SEKFV66B0S=GS1.1.1665844394.1.1.1665849398.58.0.0; _wingify_pc_uuid=fdfe2b79ad6745aea34c916a0ed6593c; __tid=uid-8271807831.2962218641; _sp_srt_id.b17c=9d06db3f-4e9a-4a76-a92c-c62010ebc888.1665845234.2.1665849403.1665846110.21b0e5d2-d867-4bde-b8c4-68dc9de23209; _ga=GA1.2.1290975728.1665845236; tryMetamaskHide=true; _gid=GA1.2.336080138.1665845260; fs_uid=#BN5B8#4935986190192640:5498079595433984:::#/1697381259; fs_cid=1.0; adformfrpid=5312976836832772683; wingify_donot_track_actions=0; g_state={"i_p":1665853302430,"i_l":1}; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRhYzRhNmMwNzcyMjQ4NGIxNzZhNWI=; __cf_bm=ePgheGZhao__qyAp6kskGwBClsgm1Dx8KTAKto.zCF4-1665853899-0-AXtuZZReE9x21qftHBWSK8X2/uqstGRh0S35oxy7GAi7PKHbOBi5o6KRnZ57jwAy3nwmK+tyMucsT012tbpRRow='
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
        self.sports = {}
        self.paises = {}
        self.campeonatos = {}
        self.scraper = cloudscraper.create_scraper()
        self.proxy = {'https': 'http://127.0.0.1:12960'}
    def get_dados(self):
        self.get_all_sports()
        self.get_all_camp()

    def get_all_sports(self):
        url = 'https://sportsbet.io/pt/sports'
        headers = {
            'Host': 'sportsbet.io',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Accept-Encoding': 'gzip, deflate, br',
            #'Referer': 'https://sportsbet.io/pt/sports',
            'Cookie': self.cookies,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        html_text = get_url_str(url=url, headers=headers).text
        soup = BeautifulSoup(html_text, 'html.parser')
        headers = {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': f'https://sportsbet.io/pt/sports/soccer/matches/future',
            'content-type': 'application/json',
            'Origin': 'https://sportsbet.io',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cookie': self.cookies
        }
        data = {"operationName": "SportEventListQuery",
                "variables": {"language": "pt", "site": "sportsbet", "slug": 'soccer',
                              "timePeriod": "ANY", "leagueTournaments": "ANY", "featuredLeagueTournaments": "ANY",
                              "tournamentEventCount": "ANY"},
                "query": "query SportEventListQuery($language: String!, $slug: String!, $timePeriod: SportsbetNewGraphqlSportLeagues!, $leagueTournaments: SportsbetNewGraphqlLeagueTournaments!, $featuredLeagueTournaments: SportsbetNewGraphqlFeaturedLeagueTournaments!, $tournamentEventCount: SportsbetNewGraphqlTournamentEventCount!, $site: String) {\n  sportsbetNewGraphql {\n    id\n    getSportBySlug(slug: $slug, site: $site) {\n      id\n      slug\n      featuredLeague {\n        id\n        name(language: $language)\n        tournaments(childType: $featuredLeagueTournaments) {\n          id\n          slug\n          name(language: $language)\n          eventCount(childType: $tournamentEventCount)\n          league {\n            id\n            slug\n            name(language: $language)\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      name(language: $language)\n      leagues(childType: $timePeriod) {\n        id\n        name(language: $language)\n        slug\n        tournaments(childType: $leagueTournaments) {\n          id\n          slug\n          name(language: $language)\n          eventCount(childType: $tournamentEventCount)\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        response_json = post_url_str(url=url, headers=headers, data=data)

        for link in soup.find_all('script'):
            if 'window.APOLLO_STATE=' in link.text:
                data = link.text
                start = data.find('window.APOLLO_STATE=JSON.parse("') + len('window.APOLLO_STATE=JSON.parse("')
                end = data.find('window.APPLICATION_CONTEXT=JSON.parse("')
                substring = data[start:end].strip()[:-3]
                data_json = json.loads(codecs.decode(substring, 'unicode_escape'))
                for t in data_json:
                    if '__typename' in data_json[t] and data_json[t]['__typename'] == 'SportsbetNewGraphqlSportCategory':
                        nome = data_json[t]['name({"language":"pt"})'].strip()
                        insert_sports(self, nome.encode("latin-1").decode("utf-8"), data_json[t]['slug'], data_json[t]['id'])
                        # sqlgg = f'SELECT id from ind_sports WHERE sport_name="{nomex}";'
                        # check_ind = self.conexao.bd(sqlgg, fetch=True)
                        # if check_ind:
                        #     sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, id_ind_sport, slug) VALUES ({self.id_site},"{id}","{nomex}", {check_ind[0][0]},"{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
                        # else:
                        #     sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, slug) VALUES ({self.id_site},"{id}","{nomex}", "{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
                        # id_bd = self.conexao.bd(sqlxx, fetch=False)
                        # if id_bd == 0:
                        #     t_id_bd = self.conexao.bd(f'SELECT id FROM sit_sports WHERE id_site = {self.id_site} and id_site_sport = "{id}"', fetch=True)
                        #     if t_id_bd: id_bd = t_id_bd[0][0]
                        # self.sports[nomex] = {'nome': nomex, 'slug': slug, 'id_bd': id_bd, 'id_site': id}

    def get_all_camp(self):
        url = 'https://sportsbet.io/graphql'
        for e in self.sports:
            headers = {
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                'Referer': f'https://sportsbet.io/pt/sports/{self.sports[e]["slug"]}/matches/future',
                'content-type': 'application/json',
                'Origin': 'https://sportsbet.io',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Cookie': self.cookies
            }
            data = {"operationName":"SportEventListQuery","variables":{"language":"pt","site":"sportsbet","slug": self.sports[e]['slug'],"timePeriod":"ANY","leagueTournaments":"ANY","featuredLeagueTournaments":"ANY","tournamentEventCount":"ANY"},"query":"query SportEventListQuery($language: String!, $slug: String!, $timePeriod: SportsbetNewGraphqlSportLeagues!, $leagueTournaments: SportsbetNewGraphqlLeagueTournaments!, $featuredLeagueTournaments: SportsbetNewGraphqlFeaturedLeagueTournaments!, $tournamentEventCount: SportsbetNewGraphqlTournamentEventCount!, $site: String) {\n  sportsbetNewGraphql {\n    id\n    getSportBySlug(slug: $slug, site: $site) {\n      id\n      slug\n      featuredLeague {\n        id\n        name(language: $language)\n        tournaments(childType: $featuredLeagueTournaments) {\n          id\n          slug\n          name(language: $language)\n          eventCount(childType: $tournamentEventCount)\n          league {\n            id\n            slug\n            name(language: $language)\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      name(language: $language)\n      leagues(childType: $timePeriod) {\n        id\n        name(language: $language)\n        slug\n        tournaments(childType: $leagueTournaments) {\n          id\n          slug\n          name(language: $language)\n          eventCount(childType: $tournamentEventCount)\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
            response_json = post_url_json(url=url, headers=headers, data=data)
            dados = response_json['data']['sportsbetNewGraphql']['getSportBySlug']
            if 'featuredLeague' in dados and 'tournaments' in dados['featuredLeague']:
                for t in dados['featuredLeague']['tournaments']:
                    if 'league' in t and not t['league']['slug'] in self.paises:
                        insert_pais(self, t["league"]["name"].strip(), t["league"]["slug"], t["league"]["id"])
                        # sqlgg = f'SELECT id from ind_paises WHERE pais_name="{t["league"]["name"].strip()}";'
                        # check_ind = self.conexao.bd(sqlgg, fetch=True)
                        # if check_ind:
                        #     sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, id_ind_pais, slug) VALUES ({self.id_site},"{t["league"]["id"]}","{t["league"]["name"].strip()}",{check_ind[0][0]},"{t["league"]["slug"]}") ON DUPLICATE KEY UPDATE site_pais_name="{t["league"]["name"].strip()}", slug="{t["league"]["slug"]}";'
                        # else:
                        #     sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, slug) VALUES ({self.id_site},"{t["league"]["id"]}","{t["league"]["name"].strip()}","{t["league"]["slug"]}") ON DUPLICATE KEY UPDATE site_pais_name="{t["league"]["name"].strip()}", slug="{t["league"]["slug"]}";'
                        # id_bd = self.conexao.bd(sqlxx, fetch=False)
                        # if id_bd == 0:
                        #     t_id_bd = self.conexao.bd(f'SELECT id FROM sit_paises WHERE id_site = {self.id_site} and id_site_pais="{t["league"]["id"]}"', fetch=True)
                        #     if t_id_bd: id_bd = t_id_bd[0][0]
                        # self.paises[t["league"]["slug"]] = {'name': t["league"]["name"].strip(), 'id_bd': id_bd, 'id_site': t["league"]["id"]}

                    if not t['slug'] in self.campeonatos:
                        insert_camp(self, t['name'].strip(), t['slug'], t['id'], self.sports[e], self.paises[t["league"]["slug"]])

                        # self.campeonatos[t['slug']] = {'name': t['name'].strip(), 'id': t['id']}
                        # sqlxx = f'INSERT INTO sit_camp (id_site, id_site_sport, id_site_pais, id_site_camp, site_camp_name, slug) VALUES ({self.id_site}, {self.sports[e]["id_bd"]}, {self.paises[t["league"]["slug"]]["id_bd"]}, "{t["id"]}","{t["name"].strip()}","{t["slug"]}") ON DUPLICATE KEY UPDATE site_camp_name="{t["name"]}", slug="{t["slug"]}";'
                        # self.conexao.bd(sqlxx, fetch=False)

            if 'leagues' in dados:
                for p in dados['leagues']:
                    if not p['slug'] in self.paises:
                        insert_pais(self, p["name"].strip(), p["slug"], p["id"])
                        # sqlgg = f'SELECT id from ind_paises WHERE pais_name="{p["name"]}";'
                        # check_ind = self.conexao.bd(sqlgg, fetch=True)
                        # if check_ind:
                        #     sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, id_ind_pais, slug) VALUES ({self.id_site},"{p["id"]}","{p["name"].strip()}",{check_ind[0][0]},"{p["slug"]}") ON DUPLICATE KEY UPDATE site_pais_name="{p["name"].strip()}", slug="{p["slug"]}";'
                        # else:
                        #     sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, slug) VALUES ({self.id_site},"{p["id"]}","{p["name"].strip()}","{p["slug"]}") ON DUPLICATE KEY UPDATE site_pais_name="{p["name"].strip()}", slug="{p["slug"]}";'
                        # id_bd = self.conexao.bd(sqlxx, fetch=False)
                        # if id_bd == 0:
                        #     t_id_bd = self.conexao.bd(f'SELECT id FROM sit_paises WHERE id_site = {self.id_site} and id_site_pais="{p["id"]}"', fetch=True)
                        #     if t_id_bd: id_bd = t_id_bd[0][0]
                        # self.paises[p["slug"]] = {'name': p["name"].strip(), 'id_bd': id_bd, 'id_site': p["id"]}
                    for t in p['tournaments']:
                        if not t['slug'] in self.campeonatos and t['name'] != None:
                            insert_camp(self, t['name'].strip(), t['slug'], t['id'], self.sports[e], self.paises[p["slug"]])
                            # self.campeonatos[t['slug']] = {'name': t['name'].strip(), 'id': t['id']}
                            # sqlxx = f'INSERT INTO sit_camp (id_site, id_site_sport, id_site_pais, id_site_camp, site_camp_name, slug) VALUES ({self.id_site},{self.sports[e]["id_bd"]}, {self.paises[p["slug"]]["id_bd"]}, "{t["id"]}","{t["name"].strip()}","{t["slug"]}") ON DUPLICATE KEY UPDATE site_camp_name="{t["name"].strip()}", slug="{t["slug"]}";'
                            # self.conexao.bd(sqlxx, fetch=False)
            xxx = 0
            # for e in response_json['data']:
            #     for e1 in response_json['data'][e]:
            #         xx = response_json['data'][e][e1]
            #         xxx = 0
            #
