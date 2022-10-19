from concurrent.futures import ThreadPoolExecutor
from acessos import *
from bs4 import BeautifulSoup
import codecs, html, json, time
import cloudscraper
from cookie import *
class c_sportsbet:
    def __init__(self, conexao):
        self.sessao = requests.session()
        self.id_site = 2
        self.mysql_conn = conexao
        self.cookies = '__cfwaitingroom=Chh4SUdKOEIvL3A2dEpuUGZLWWpxU2RBPT0SkAJJQlBhbEJIUEFzMjNDZlVKZlQ5czZJd2tvVlM3Wk85bEpNbDloS2VPSnNkQXBKa2Fkd2Vud0Z0NTAyandtWHZlVXl1Z1Y1ODF2SXRPRW9Sd0Q2UXU5Wk9hMEVnNXZpU3dtSWJIMHBRcWgrb0NMN08xRXlVMzBRcmVlMlVMV0Fnb0YwSmNBS2l4TVpZK2d0OVRYTTg2QXI5MGtud1lEejJJR2hOa3NHN29PbFJuK1NxckZHak1kQmNvc1JRZ3FoZzZOTThySGllZElWQ2RkWHRJaUh3Y2YvOTF1R3l2TkdoNitOL1dkRVNNei9BNVAyUmF3UWtnMFJmK3dMR3ZuK3J6dmtOSURmblNIQWc0emtKNA%3D%3D; _ga_SEKFV66B0S=GS1.1.1666120922.5.0.1666120922.60.0.0; _wingify_pc_uuid=fdfe2b79ad6745aea34c916a0ed6593c; __tid=uid-8271807831.2962218641; _sp_srt_id.b17c=9d06db3f-4e9a-4a76-a92c-c62010ebc888.1665845234.5.1666118246.1666115462.6cd15c9f-79ea-4ace-b908-954a36708154; _ga=GA1.2.1290975728.1665845236; tryMetamaskHide=true; fs_uid=#BN5B8#4935986190192640:4955098419007488:::#/1697381259; fs_cid=1.0; adformfrpid=5312976836832772683; wingify_donot_track_actions=0; g_state={"i_p":1666721925579,"i_l":3}; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; _gid=GA1.2.1016127202.1666115464; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRhYzRhNmMwNzcyMjQ4NGIxNzZhNWI=; __cf_bm=wA2ut61F1buOGqB6yH6n2RYBpR.d2E3lwhWA0bMudt8-1666120924-0-Adz1Qtsa2YQlbKzZ9U8jOCApkeh5TdgvEiZnB+qrby1PykOxoSc0AgSbeOUljC0ebquimOUToTCiuBtjtPDDDPY='
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
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Accept-Encoding': 'gzip, deflate, br',
            #'Referer': 'https://sportsbet.io/pt/sports',
            'Cookie': self.cookies,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        cookies = ler_cookies()
        time1 = str(int(time.time()))
        time2 = str(int(time.time())+1)
        cookie_new = '_fs_tab_id=c098b7e0d6e030;__cfwaitingroom=Chh4SUdKOEIvL3A2dEpuUGZLWWpxU2RBPT0SkAJJQlBhbEJIUEFzMjNDZlVKZlQ5czZJd2tvVlM3Wk85bEpNbDloS2VPSnNkQXBKa2Fkd2Vud0Z0NTAyandtWHZlVXl1Z1Y1ODF2SXRPRW9Sd0Q2UXU5Wk9hMEVnNXZpU3dtSWJIMHBRcWgrb0NMN08xRXlVMzBRcmVlMlVMV0Fnb0YwSmNBS2l4TVpZK2d0OVRYTTg2QXI5MGtud1lEejJJR2hOa3NHN29PbFJuK1NxckZHak1kQmNvc1JRZ3FoZzZOTThySGllZElWQ2RkWHRJaUh3Y2YvOTF1R3l2TkdoNitOL1dkRVNNei9BNVAyUmF3UWtnMFJmK3dMR3ZuK3J6dmtOSURmblNIQWc0emtKNA%3D%3D; _ga_SEKFV66B0S=GS1.1.1666120922.5.0.' + time2  + '.60.0.0; _wingify_pc_uuid=fdfe2b79ad6745aea34c916a0ed6593c; __tid=uid-8271807831.2962218641; _sp_srt_id.b17c=9d06db3f-4e9a-4a76-a92c-c62010ebc888.1665845234.6.' + time1 + '.1666118246.f8b561b9-65df-4985-9a9b-b4b4950cf68d; _ga=GA1.2.1290975728.1665845236; tryMetamaskHide=true; fs_uid=#BN5B8#4935986190192640:4955098419007488:::#/1697381259; fs_cid=1.0; adformfrpid=5312976836832772683; wingify_donot_track_actions=0; g_state={"i_p":1666721925579,"i_l":3}; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; _gid=GA1.2.1016127202.1666115464; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRhYzRhNmMwNzcyMjQ4NGIxNzZhNWI=; __cf_bm=wA2ut61F1buOGqB6yH6n2RYBpR.d2E3lwhWA0bMudt8-1666120924-0-Adz1Qtsa2YQlbKzZ9U8jOCApkeh5TdgvEiZnB+qrby1PykOxoSc0AgSbeOUljC0ebquimOUToTCiuBtjtPDDDPY='
        cookie_new2= '_wingify_pc_uuid=fdfe2b79ad6745aea34c916a0ed6593c; __tid=uid-8271807831.2962218641; _sp_srt_id.b17c=9d06db3f-4e9a-4a76-a92c-c62010ebc888.1665845234.6.'+ time1+'.1666118246.f8b561b9-65df-4985-9a9b-b4b4950cf68d; tryMetamaskHide=true; fs_uid=#BN5B8#4935986190192640:6491650097909760:::#/1697381259; fs_cid=1.0; adformfrpid=5312976836832772683; wingify_donot_track_actions=0; g_state={"i_p":1666721925579,"i_l":3}; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; refAff=affid=148&cxid=148_390538&source=834dde61122; _ga=GA1.2.9566590343.5008065082; _gid=GA1.2.1327268174.1666120956; _ga_SEKFV66B0S=GS1.1.1666120922.5.1.' + time2 + '.59.0.0; GW_CLIENT_ID=40044fa102acb6931773f9360c70e283567eaf87ea7c4b89903a7a877fa08a4a; __cf_bm=Ln.Y1No9IXJFQpjhDKUY.WlPuJEJZtSgZ84fuOw6kvE-1666128101-0-AavS/k5pOAmxrYDj8esgJL23FzifJ7GjEgOyhW+k4fZCCbBQAMG0YpC/Kxj4hg3MHaI+ohbLrYinCwyjso54zGU=; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRhYzRhNmMwNzcyMjQ4NGIxNzZhNWI='
        cookie_new3 = 'experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; __cf_bm=9sbw_fRdetRON3Wjow7ly1g.J8IFlnthW9ptWMbQ8ho-1666128904-0-ATMuKJ5hzL8s134AhK3K/DPVoaRAPYB2p/hUJ+J2/ME3NDCw4rnO67waTOWgsQuNgRrMpCVfvXOfTMSn+tIG165CKjfL0SlznbiiUriwqPSXQsyuZuyKm3mCFI8l1g63uKoAhjnAb1npnOwDdPqx6otS00EA2w2Mj9csG79ylN3I; MKTSRC={"t":1666128900100,"d":{"src":"direct","mdm":"direct","cmp":"","kwd":"","cnt":"","glc":"","msc":""}}; _dd_s=rum=1&id=dc45aae9-96bb-46fe-8179-b46d2bf10706&created=1666128900587&expire=1666129925735&logs=1; _wingify_pc_uuid=c294ceb68ad8497b8289e1ef8b2d0b0e; __tid=uid-7391421832.7179433751; _ga_SEKFV66B0S=GS1.1.1666128903.1.1.1666128926.37.0.0; _ga=GA1.2.1039401276.1666128903; _sp_srt_ses.b17c=*; _sp_srt_id.b17c=42aeeb8c-d7a9-4532-91a8-937e2a30feeb.1666128903.1.1666128925.1666128903.f932475b-84a3-4a2c-85e9-e27a4bf8f5d8; GW_CLIENT_ID=90a8bb8c57052b0cd7bd6b450c43fc5cd2f8ee09d324114126c240ba5e204dc5; _gid=GA1.2.581277808.1666128908; adformfrpid=381027116410573887; fs_uid=#BN5B8#6367371768336384:5049902054215680:::#/1697664908; fs_cid=1.0; wingify_donot_track_actions=0; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRmMWMwMTY0MGNkYjZlMWZjNDM1ZWY='
        headersX = {'Host': 'sportsbet.io',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Cookie': cookie_new3,
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1'}
        urlf = "https://sportsbet.io/pt/sports"
        tester = requests.get(url=urlf, headers=headersX)

        urlxx = "http://2captcha.com/in.php?key=0a8b7adcaded3fb07836cb56a47b111f&method=userrecaptcha&version=v3&action=verify&min_score=0.3&googlekey=6LeljvsfAAAAACR46bzAIy6Cukry12i-LpJe7U_H&pageurl=https://sportsbet.io/pt/sports"
        tester = self.sessao.get(url=urlxx, allow_redirects=True)

        html_text = get_url_str(self, url=url, headers=headers).text
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
        response_json = post_url_str(self, url=url, headers=headers, data=data)

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
