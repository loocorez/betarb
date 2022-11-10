from acessos import *
from bs4 import BeautifulSoup
import codecs, json, time
from datetime import datetime
from playwright.sync_api import sync_playwright
import urllib.request
class c_stake:
    def __init__(self, conexao):
        self.sessao = requests.session()
        self.id_site = 4
        self.site_name = "STAKE.COM"
        self.mysql_conn = conexao
        #self.cookies = '__cfwaitingroom=Chh4SUdKOEIvL3A2dEpuUGZLWWpxU2RBPT0SkAJJQlBhbEJIUEFzMjNDZlVKZlQ5czZJd2tvVlM3Wk85bEpNbDloS2VPSnNkQXBKa2Fkd2Vud0Z0NTAyandtWHZlVXl1Z1Y1ODF2SXRPRW9Sd0Q2UXU5Wk9hMEVnNXZpU3dtSWJIMHBRcWgrb0NMN08xRXlVMzBRcmVlMlVMV0Fnb0YwSmNBS2l4TVpZK2d0OVRYTTg2QXI5MGtud1lEejJJR2hOa3NHN29PbFJuK1NxckZHak1kQmNvc1JRZ3FoZzZOTThySGllZElWQ2RkWHRJaUh3Y2YvOTF1R3l2TkdoNitOL1dkRVNNei9BNVAyUmF3UWtnMFJmK3dMR3ZuK3J6dmtOSURmblNIQWc0emtKNA%3D%3D; _ga_SEKFV66B0S=GS1.1.1666120922.5.0.1666120922.60.0.0; _wingify_pc_uuid=fdfe2b79ad6745aea34c916a0ed6593c; __tid=uid-8271807831.2962218641; _sp_srt_id.b17c=9d06db3f-4e9a-4a76-a92c-c62010ebc888.1665845234.5.1666118246.1666115462.6cd15c9f-79ea-4ace-b908-954a36708154; _ga=GA1.2.1290975728.1665845236; tryMetamaskHide=true; fs_uid=#BN5B8#4935986190192640:4955098419007488:::#/1697381259; fs_cid=1.0; adformfrpid=5312976836832772683; wingify_donot_track_actions=0; g_state={"i_p":1666721925579,"i_l":3}; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; _gid=GA1.2.1016127202.1666115464; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRhYzRhNmMwNzcyMjQ4NGIxNzZhNWI=; __cf_bm=wA2ut61F1buOGqB6yH6n2RYBpR.d2E3lwhWA0bMudt8-1666120924-0-Adz1Qtsa2YQlbKzZ9U8jOCApkeh5TdgvEiZnB+qrby1PykOxoSc0AgSbeOUljC0ebquimOUToTCiuBtjtPDDDPY='
        #self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
        self.sports = {}
        self.paises = {}
        self.campeonatos = {}
        self.eventos = {}
        self.competidores = {}
        self.mercados = {}
        self.add_ind = False
        self.proxy = {'server': '127.0.0.1:12960'}
        self.p = sync_playwright().start()
        self.browser = self.p.firefox.launch(headless=False, proxy=self.proxy)
        self.context = self.browser.new_context(base_url="https://stake.com", ignore_https_errors=True, locale="pt-BR")
        self.page = self.context.new_page()
        self.first_acess()
        self.get_data()
    def get_data(self):
        for sport in self.sports:
            print(f'{self.site_name} - Capturando dados esporte: {self.sports[sport]["name"]}...')
            post_sport_data = {"query":"query TournamentTableList($sport: String!) {\n  slugSport(sport: $sport) {\n    id\n    name\n    slug\n    categoryList(limit: 100, type: active) {\n      id\n      name\n      slug\n      fixtureCount(type: active)\n      tournamentList(limit: 50, type: active) {\n        id\n        name\n        slug\n        fixtureCount(type: active)\n      }\n    }\n  }\n}\n","variables":{"sport": sport}}
            sport_data = self.post_data(post_sport_data, f"https://stake.com/sports/{sport}")
            if sport_data != None and 'data' in sport_data and 'slugSport' in sport_data['data'] and 'categoryList' in sport_data['data']['slugSport']:
                for pais in sport_data['data']['slugSport']['categoryList']:
                    paisx = "" if pais["name"] == None else n_str(pais["name"].strip())
                    insert_pais(self, paisx, pais["slug"], pais["id"], add_ind=self.add_ind)
                    if 'tournamentList' in pais:
                        for camp in pais['tournamentList']:
                            campx = "" if camp['name'] == None else n_str(camp['name'].strip())
                            insert_camp(self, campx, camp['slug'], camp['id'], sport, pais["slug"], add_ind=self.add_ind)
                            post_camp_data = {"query":"query SlugTournament($sport: String!, $category: String!, $tournament: String!, $type: SportSearchEnum!, $groups: [String!]!, $limit: Int = 50, $offset: Int = 0) {\n  slugTournament(sport: $sport, category: $category, tournament: $tournament) {\n    id\n    name\n    fixtureCount(type: $type)\n    fixtureList(type: $type, limit: $limit, offset: $offset) {\n      ...FixturePreview\n      groups(groups: $groups, status: [active, suspended, deactivated]) {\n        ...SportGroupTemplates\n      }\n    }\n  }\n}\n\nfragment FixturePreview on SportFixture {\n  id\n  ...SportFixtureLiveStreamExists\n  status\n  slug\n  marketCount(status: [active, suspended])\n  extId\n  data {\n    __typename\n    ...SportFixtureDataMatch\n    ...SportFixtureDataOutright\n  }\n  tournament {\n    ...TournamentTreeNested\n  }\n  eventStatus {\n    ...SportFixtureEventStatus\n  }\n}\n\nfragment SportFixtureLiveStreamExists on SportFixture {\n  id\n  betradarStream {\n    exists\n  }\n  imgArenaStream {\n    exists\n  }\n  abiosStream {\n    exists\n    stream {\n      startTime\n      id\n    }\n  }\n  geniussportsStream(deliveryType: hls) {\n    exists\n  }\n}\n\nfragment SportFixtureDataMatch on SportFixtureDataMatch {\n  startTime\n  competitors {\n    ...SportFixtureCompetitor\n  }\n  __typename\n}\n\nfragment SportFixtureCompetitor on SportFixtureCompetitor {\n  name\n  extId\n  countryCode\n  abbreviation\n}\n\nfragment SportFixtureDataOutright on SportFixtureDataOutright {\n  name\n  startTime\n  endTime\n  __typename\n}\n\nfragment TournamentTreeNested on SportTournament {\n  id\n  name\n  slug\n  category {\n    ...CategoryTreeNested\n  }\n}\n\nfragment CategoryTreeNested on SportCategory {\n  id\n  name\n  slug\n  sport {\n    id\n    name\n    slug\n  }\n}\n\nfragment SportFixtureEventStatus on SportFixtureEventStatus {\n  homeScore\n  awayScore\n  matchStatus\n  clock {\n    matchTime\n    remainingTime\n  }\n  periodScores {\n    homeScore\n    awayScore\n    matchStatus\n  }\n  currentServer {\n    extId\n  }\n  homeGameScore\n  awayGameScore\n  statistic {\n    yellowCards {\n      away\n      home\n    }\n    redCards {\n      away\n      home\n    }\n    corners {\n      home\n      away\n    }\n  }\n}\n\nfragment SportGroupTemplates on SportGroup {\n  ...SportGroup\n  templates(limit: 50, includeEmpty: true) {\n    ...SportGroupTemplate\n    markets(limit: 1) {\n      ...SportMarket\n      outcomes {\n        ...SportMarketOutcome\n      }\n    }\n  }\n}\n\nfragment SportGroup on SportGroup {\n  name\n  translation\n  rank\n}\n\nfragment SportGroupTemplate on SportGroupTemplate {\n  extId\n  rank\n  name\n}\n\nfragment SportMarket on SportMarket {\n  id\n  name\n  status\n  extId\n  specifiers\n  customBetAvailable\n}\n\nfragment SportMarketOutcome on SportMarketOutcome {\n  active\n  id\n  odds\n  name\n  customBetAvailable\n}\n","variables":{"type":"popular","tournament": camp['slug'],"category":pais['slug'],"sport":"soccer","groups":["main", "goals", "1st2ndhalfmarkets", "AsianLines"],"limit":50,"offset":0}}
                            camp_data = self.post_data(post_camp_data, f"https://stake.com/sports/{sport}")
                            valores_sql = ""
                            if camp_data != None and camp_data['data']['slugTournament'] != None and 'fixtureList' in camp_data['data']['slugTournament']:
                                for event in camp_data['data']['slugTournament']['fixtureList']:
                                    if 'data' in event and 'eventStatus' in event and 'competitors' in event['data'] and len(event['data']['competitors']) == 2:
                                        if event['eventStatus']['matchStatus'] == 'Por iniciar':
                                            status = 1
                                        else:
                                            status = 2
                                        nome_casa = event['data']['competitors'][0]['name']
                                        nome_visitante = event['data']['competitors'][1]['name']
                                        eventx = n_str(f'{nome_casa} - {nome_visitante}')
                                        start_timex = datetime.strptime(event['data']['startTime'], "%a, %d %b %Y %H:%M:%S GMT")
                                        start_time = start_timex.strftime('%Y-%m-%d %H:%M:%S')
                                        insert_event(self, start_time, eventx, event['slug'], event['id'], status, sport, pais["slug"], camp["slug"], add_ind=self.add_ind)

                                        insert_compet(self, sport, event['id'], event['data']['competitors'][0]['extId'], n_str(event['data']['competitors'][0]['name']), 1, add_ind=self.add_ind)
                                        insert_compet(self, sport, event['id'], event['data']['competitors'][1]['extId'], n_str(event['data']['competitors'][1]['name']), 2, add_ind=self.add_ind)
                                        if 'groups' in event:
                                            for groups in event['groups']:
                                                if 'templates' in groups:
                                                    for templates in groups['templates']:
                                                        fillname = False

                                                        marketx = n_str(templates['name'])

                                                        if '{$competitor1}' in marketx or '{$competitor2}' in marketx:
                                                            fillname = True
                                                            marketx = marketx.replace('{$competitor1}', "|Casa|")
                                                            marketx = marketx.replace('{$competitor2}', "|Visitante|")
                                                        if '{!goalnr} gol' == marketx:
                                                            fillname = True
                                                            marketx = 'Próximos gols'#marketx.replace('{$competitor1}', "|Casa|")

                                                        if 'markets' in templates:
                                                            for market in templates['markets']:
                                                                if not fillname:
                                                                    marketx = market['name']
                                                                if not (sport, templates['extId']) in self.mercados:
                                                                    if market['status'] == 'active':
                                                                        status = 1
                                                                    else:
                                                                        status = 0
                                                                    insert_mercado(self, sport, templates["extId"], marketx,
                                                                                   templates['name'],
                                                                                   status, 1,
                                                                                   add_ind=self.add_ind)

                                                                if 'outcomes' in market and self.mercados[(sport, templates["extId"])]['ativo'] == 1:
                                                                    for selecao in market['outcomes']:
                                                                        selecaox = n_str(selecao['name'])
                                                                        if nome_casa in selecaox:
                                                                            selecaox = selecaox.replace(nome_casa, "|Casa|")
                                                                        if nome_visitante in selecaox:
                                                                            selecaox = selecaox.replace(nome_visitante, "|Visitante|")
                                                                        insert_selecao(self, sport, templates["extId"], selecaox, add_ind=self.add_ind)
                                                                        if valores_sql != "": valores_sql += ", "
                                                                        valores_sql += f'({self.eventos[event["id"]]["id_bd"]}, {self.mercados[(sport, templates["extId"])]["selecoes"][selecaox]["id_bd"]}, "{n_str(selecao["name"])}", "{selecao["odds"]}", "{selecao["id"]}")'

                                    else:
                                        xxx = 0
                                if valores_sql != "":
                                    sqlxx = f'INSERT INTO sit_events_odds (id_sit_evento, id_sit_selecao, selecao_nome2, odd, site_id_selecao) ' \
                                            f'VALUES {valores_sql} ON DUPLICATE KEY ' \
                                            f'UPDATE odd=VALUES(odd);'
                                    id_bd = self.mysql_conn.bd(sqlxx, fetch=False)

                                time.sleep(10)
                                xxx = 0
            else:
                xxx = 0


    def post_data(self, datapost, referrer):
        try:
            cookies = self.page.context.cookies()
            string_cookies = ""
            for c in cookies:
                if 'stake.com' in c['domain']:
                    string_cookies += f"{c['name']}={c['value']};"
            req = urllib.request.Request("https://sportsbet.io/_api/graphql")
            req.set_proxy('localhost:12960', 'http')
            jsondataasbytes = json.dumps(datapost).encode('utf-8')
            req.add_header('Host', 'stake.com')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0')
            req.add_header('Accept', '*/*')
            req.add_header('Accept-Language', 'pt-BR')
            req.add_header('Accept-Encoding', 'gzip, deflate, br')
            req.add_header('Referer', referrer)
            req.add_header('cf-device-type', '')
            req.add_header('x-forwarded-for', '187.19.130.235, 172.70.193.134, 172.20.227.78')
            req.add_header('x-geoip-country', 'BR')
            req.add_header('x-geoip-state', 'BR-PB')
            req.add_header('content-type', 'application/json')
            req.add_header('x-language', 'br')
            req.add_header('Content-Length', len(jsondataasbytes))
            req.add_header('Origin', 'https://stake.com')
            req.add_header('Connection', 'keep-alive')
            req.add_header('Cookie', string_cookies)
            req.add_header('Sec-Fetch-Dest', 'empty')
            req.add_header('Sec-Fetch-Mode', 'cors')
            req.add_header('Sec-Fetch-Site', 'same-origin')
            with urllib.request.urlopen(req, jsondataasbytes) as f:
                res = f.read()
            response = res.decode()
            json_s = json.loads(response)
            return json_s
        except Exception as e:
            print(e)
            return None
    def first_acess(self):
        self.page.set_viewport_size({'width': 1920, 'height': 870})
        self.page.goto("/", wait_until="domcontentloaded")
        script_find = self.page.locator('[data-body="1e8v2xn"]').first.inner_text()
        self.page.wait_for_load_state('domcontentloaded')
        data_json = json.loads(script_find)
        data_json2 = json.loads(data_json['body'])
        for d in data_json2['data']['sportList']:
            insert_sports(self, d['name'], d['slug'], d['id'])

        # data_json = json.loads(kkk)
        # html_text = self.page.inner_html('*')
        # soup = BeautifulSoup(html_text, 'html.parser')
        # for link in soup.find_all('script'):
        #     if 'data-url' in link:
        #         tt = link['data-url']
        #         d_body = link['data-body']
        #         if tt == "https://stake.com/_api/graphql":
        #             xxx = 0
        #     if 'window.APOLLO_STATE=' in link.text:
        #         data = link.text
        #         start = data.find('window.APOLLO_STATE=JSON.parse("') + len('window.APOLLO_STATE=JSON.parse("')
        #         end = data.find('window.APPLICATION_CONTEXT=JSON.parse("')
        #         substring = data[start:end].strip()[:-3]
        #         data_json = json.loads(codecs.decode(substring, 'unicode_escape'))
        #         for t in data_json:
        #             if '__typename' in data_json[t] and data_json[t][
        #                 '__typename'] == 'SportsbetNewGraphqlSportCategory':
        #                 nome = data_json[t]['name({"language":"pt"})'].strip()
        #                 insert_sports(self, nome.encode("latin-1").decode("utf-8"), data_json[t]['slug'],
        #                               data_json[t]['id'])