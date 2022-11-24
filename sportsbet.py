from acessos import *
from bs4 import BeautifulSoup
import codecs, json, time
from playwright.sync_api import sync_playwright
from datetime import  datetime
import urllib.request
import requests
class c_sportsbet:
    def __init__(self, conexao):
        self.sessao = requests.session()
        self.id_site = 3
        self.site_name = "SPORTSBET.IO"
        self.add_ind = True
        self.mysql_conn = conexao
        #self.cookies = '__cfwaitingroom=Chh4SUdKOEIvL3A2dEpuUGZLWWpxU2RBPT0SkAJJQlBhbEJIUEFzMjNDZlVKZlQ5czZJd2tvVlM3Wk85bEpNbDloS2VPSnNkQXBKa2Fkd2Vud0Z0NTAyandtWHZlVXl1Z1Y1ODF2SXRPRW9Sd0Q2UXU5Wk9hMEVnNXZpU3dtSWJIMHBRcWgrb0NMN08xRXlVMzBRcmVlMlVMV0Fnb0YwSmNBS2l4TVpZK2d0OVRYTTg2QXI5MGtud1lEejJJR2hOa3NHN29PbFJuK1NxckZHak1kQmNvc1JRZ3FoZzZOTThySGllZElWQ2RkWHRJaUh3Y2YvOTF1R3l2TkdoNitOL1dkRVNNei9BNVAyUmF3UWtnMFJmK3dMR3ZuK3J6dmtOSURmblNIQWc0emtKNA%3D%3D; _ga_SEKFV66B0S=GS1.1.1666120922.5.0.1666120922.60.0.0; _wingify_pc_uuid=fdfe2b79ad6745aea34c916a0ed6593c; __tid=uid-8271807831.2962218641; _sp_srt_id.b17c=9d06db3f-4e9a-4a76-a92c-c62010ebc888.1665845234.5.1666118246.1666115462.6cd15c9f-79ea-4ace-b908-954a36708154; _ga=GA1.2.1290975728.1665845236; tryMetamaskHide=true; fs_uid=#BN5B8#4935986190192640:4955098419007488:::#/1697381259; fs_cid=1.0; adformfrpid=5312976836832772683; wingify_donot_track_actions=0; g_state={"i_p":1666721925579,"i_l":3}; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; _gid=GA1.2.1016127202.1666115464; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRhYzRhNmMwNzcyMjQ4NGIxNzZhNWI=; __cf_bm=wA2ut61F1buOGqB6yH6n2RYBpR.d2E3lwhWA0bMudt8-1666120924-0-Adz1Qtsa2YQlbKzZ9U8jOCApkeh5TdgvEiZnB+qrby1PykOxoSc0AgSbeOUljC0ebquimOUToTCiuBtjtPDDDPY='
        #self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
        self.sports = {}
        self.paises = {}
        self.campeonatos = {}
        self.eventos = {}
        self.competidores = {}
        self.mercados = {}
        self.proxy = {'server': '127.0.0.1:12960'}
        self.p = sync_playwright().start()
        self.browser = self.p.firefox.launch(headless=False, proxy=self.proxy)
        self.context = self.browser.new_context(base_url="https://sportsbet.io", ignore_https_errors=True, locale="pt-BR")
        self.page = self.context.new_page()
        #self.page.__setattr__('_allowInterception', True)
        self.first_acess()

    def get_data(self, sim=False):
        if sim:
            with open(f"./jsons/esportes.json") as json_file:
                self.sports = json.load(json_file)
        else:
            with open(f"./jsons/esportes.json", "w") as outfile:
                json.dump(self.sports, outfile)
        for sport in self.sports:
            print(f'{self.site_name} - Capturando dados esporte: {self.sports[sport]["name"]}...')
            datapost = {"operationName": "SportQuery",
                        "variables": {"language": "pt", "site": "sportsbet", "slug": sport, "timePeriod": "ANY",
                                      "leagueTournaments": "ANY"},
                        "query": "query SportQuery($language: String!, $slug: String!, $site: String) {\n  sportsbetNewGraphql {\n    id\n    getSportBySlug(slug: $slug, site: $site) {\n      id\n      slug\n      name(language: $language)\n      enName: name(language: \"en\")\n      leagues(childType: ANY) {\n        id\n        slug\n        name(language: $language)\n        tournaments(childType: ANY) {\n          id\n        slug\n        name(language: $language)\n          events(childType: ANY, first: 1) {\n            id\n        slug\n        name(language: $language)\n  status\n  start_time\n  market_count\n  live_odds\n  competitors {\n    id\n    name\n    type\n  }\n      mainMarkets {\n        ...MainEventMarketFragment\n      }\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment MainEventMarketFragment on SportsbetNewGraphqlMarket {\n  id\n  name(language: $language)\n  englishName: name(language: \"en\")\n  enName: name(language: \"en\")\n  status\n  selections {\n    ...ListEventMarketSelectionFragment\n  }\n  market_type {\n    id\n    name\n    description\n    translation_key\n    type\n    settings {\n      id\n      betBoostMultiplier\n    }\n  }\n  specifiers\n}\n\nfragment ListEventMarketSelectionFragment on SportsbetNewGraphqlMarketSelection {\n  id\n  name(language: $language)\n  enName: name(language: \"en\")\n  active\n  odds\n  probabilities\n  providerProductId\n}\n"}
            if sim:
                with open(f"./jsons/{sport}.json") as json_file:
                    retorno = json.load(json_file)
            else:
                retorno = self.post_data(datapost)
                with open(f"./jsons/{sport}.json", "w") as outfile:
                    json.dump(retorno, outfile)
            if retorno != None and 'data' in retorno and 'sportsbetNewGraphql' in retorno['data'] and 'getSportBySlug' in retorno['data']['sportsbetNewGraphql'] and 'leagues' in retorno['data']['sportsbetNewGraphql']['getSportBySlug']:
                for pais in retorno['data']['sportsbetNewGraphql']['getSportBySlug']['leagues']:
                    paisx = "" if pais["name"] == None else n_str(pais["name"].strip())
                    insert_pais(self, paisx, pais["slug"], pais["id"], add_ind=self.add_ind)
                    valores_sql = ""
                    for camp in pais['tournaments']:
                        campx = "" if camp['name'] == None else n_str(camp['name'].strip())
                        insert_camp(self, campx, camp['slug'], camp['id'], sport, pais["slug"], add_ind=self.add_ind)
                        for event in camp['events']:
                            start_time = datetime.fromtimestamp(event['start_time'])
                            eventx = "" if event['name'] == None else n_str(event['name'].strip())
                            insert_event(self, start_time, eventx,  event['slug'], event['id'], event['status'], sport, pais["slug"], camp["slug"], add_ind=self.add_ind)
                            nome_casa = ""
                            nome_visitante = ""
                            if 'competitors' in event:
                                for compet in event['competitors']:
                                    if compet['type'] == 'home':
                                        tipo = 1
                                        nome_casa = compet['name']

                                    elif compet['type'] == 'away':
                                        tipo = 2
                                        nome_visitante = compet['name']
                                    elif compet['type'] == 'h2h':
                                        tipo = 3
                                    else:
                                        tipo = 0
                                    insert_compet(self, sport, event['id'], compet['id'], n_str(compet['name']), tipo, add_ind=self.add_ind)


                            if 'mainMarkets' in event:
                                for market in event['mainMarkets']:
                                    if market['name'] == "Handicap Asiático 0-0":
                                        xxx = 0
                                    marketx = market['name']
                                    if nome_casa in marketx:
                                        marketx = marketx.replace(nome_casa, "|Casa|")
                                    if nome_visitante in marketx:
                                        marketx = marketx.replace(nome_visitante, "|Visitante|")
                                    if marketx == "First Player To Score":
                                        xxx = 0
                                    if not (sport, market['market_type']['id']) in self.mercados:
                                        insert_mercado(self, sport, market['market_type']['id'], n_str(marketx), market['market_type']['translation_key'], market['status'], market['market_type']['type'], add_ind=self.add_ind)

                                    if 'selections' in market and self.mercados[(sport, market['market_type']['id'])]['ativo'] == 1:
                                        for selecao in market['selections']:
                                            selecaox = n_str(selecao['name'])
                                            if nome_casa in selecaox:
                                                selecaox = selecaox.replace(nome_casa, "|Casa|")
                                            if nome_visitante in selecaox:
                                                selecaox = selecaox.replace(nome_visitante, "|Visitante|")
                                            insert_selecao(self, sport, market['market_type']['id'], selecaox, add_ind=self.add_ind)
                                            if valores_sql != "": valores_sql+= ", "
                                            valores_sql += f'({self.eventos[event["id"]]["id_bd"]}, {self.mercados[(sport, market["market_type"]["id"])]["selecoes"][selecaox]["id_bd"]}, "{n_str(selecao["enName"])}", "{selecao["odds"]}", "{selecao["id"]}")'
                    if valores_sql != "":
                        sqlxx = f'INSERT INTO sit_events_odds (id_sit_evento, id_sit_selecao, selecao_nome2, odd, site_id_selecao) ' \
                                f'VALUES {valores_sql} ON DUPLICATE KEY ' \
                                f'UPDATE odd=VALUES(odd);'
                        id_bd = self.mysql_conn.bd(sqlxx, fetch=False)
                                            #insert_update_odd(self, self.eventos[event['id']]['id_bd'], self.mercados[(sport, market['market_type']['id'])]['selecoes'][selecao['id']]['id_bd'], selecao['odds'])
                                            #xx = 0
                            # self.campeonatos[t['slug']] = {'name': t['name'].strip(), 'id': t['id']}
                            # sqlxx = f'INSERT INTO sit_camp (id_site, id_site_sport, id_site_pais, id_site_camp, site_camp_name, slug) VALUES ({self.id_site},{self.sports[e]["id_bd"]}, {self.paises[p["slug"]]["id_bd"]}, "{t["id"]}","{t["name"].strip()}","{t["slug"]}") ON DUPLICATE KEY UPDATE site_camp_name="{t["name"].strip()}", slug="{t["slug"]}";'
                            # self.conexao.bd(sqlxx, fetch=False)

    # async def request_interception(self, req, datapost):
    #     """ await page.setRequestInterception(True) would block the flow, the interception is enabled individually """
    #     # enable interception
    #     req.__setattr__('_allowInterception', True)
    #     if req.url.startswith('https://sportsbet.io/graphql'):
    #         self.on_req(req, datapost)
    #         print(f"\nreq.url: {req.url}")
    #         print(f"  req.resourceType: {req.resourceType}")
    #         print(f"  req.method: POST")
    #         print(f"  req.postData: {datapost}")
    #         print(f"  req.headers: {req.headers}")
    #         print(f"  req.response: {req.response}")
    #     else:
    #         return await req.continue_()
    #
    # def on_req(self, req, postdata):
    #     req.__setattr__('_allowInterception', True)
    #     if req.url.startswith('https://sportsbet.io/graphql'):
    #         asyncio.create_task(req.continue_({
    #             "method": "POST",
    #             "postData": postdata,
    #             "headers": {
    #                 **req.headers,
    #                 "Content-Type": "application/json"
    #             }
    #         }))
    #         # asyncio.create_task(req.continue_({
    #         #     "method": "POST",
    #         #     "postData": postdata,
    #         #     "headers": {
    #         #         **req.headers,
    #         #         "Content-Type": "application/json"
    #         #     }
    #         # }))
    #
    # async def request_interception(self, req):
    #     """ await page.setRequestInterception(True) would block the flow, the interception is enabled individually """
    #     # enable interception
    #     req.__setattr__('_allowInterception', True)
    #     if req.url.startswith('https://sportsbet.io/graphql'):
    #         print(f"\nreq.url: {req.url}")
    #         print(f"  req.resourceType: {req.resourceType}")
    #         print(f"  req.method: {req.method}")
    #         print(f"  req.postData: {req.postData}")
    #         print(f"  req.headers: {req.headers}")
    #         print(f"  req.response: {req.response}")
    #     return await req.continue_()
    def post_data(self, datapost):
        try:
            cookies = self.page.context.cookies()
            string_cookies = ""
            for c in cookies:
                if 'sportsbet.io' in c['domain']:
                    if not '_gat_gtag_UA' in c['name'] or not '_gat_UA' in c['name']:
                        string_cookies += f"{c['name']}={c['value']};"
            req = urllib.request.Request("https://sportsbet.io/graphql")
            req.set_proxy('localhost:12960', 'http')
            jsondataasbytes = json.dumps(datapost).encode('utf-8')
            req.add_header('Host', 'sportsbet.io')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0')
            req.add_header('Accept', '*/*')
            req.add_header('Accept-Language', 'pt-BR')
            req.add_header('Accept-Encoding', 'gzip, deflate, br')
            req.add_header('Referer', 'https://sportsbet.io/pt/sports')
            req.add_header('content-type', 'application/json')
            req.add_header('authorization', '')
            req.add_header('Content-Length', len(jsondataasbytes))
            req.add_header('Origin', 'https://sportsbet.io')
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
        print(f'{self.site_name} - Iniciando acesso...')
        path = '/pt/sports'
        self.page.set_viewport_size({'width': 1920, 'height': 870})
        self.page.goto(path, wait_until="domcontentloaded", timeout=0)
        self.page.locator('footer').is_enabled()
        self.page.wait_for_load_state('domcontentloaded')
        html_text = self.page.inner_html('*')
        soup = BeautifulSoup(html_text, 'html.parser')
        for link in soup.find_all('script'):
            if 'window.APOLLO_STATE=' in link.text:
                data = link.text
                start = data.find('window.APOLLO_STATE=JSON.parse("') + len('window.APOLLO_STATE=JSON.parse("')
                end = data.find('window.APPLICATION_CONTEXT=JSON.parse("')
                substring = data[start:end].strip()[:-3]
                data_json = json.loads(codecs.decode(substring, 'unicode_escape'))
                print(f'{self.site_name} - Capturando indice de esportes...')
                for t in data_json:
                    if '__typename' in data_json[t] and data_json[t]['__typename'] == 'SportsbetNewGraphqlSportCategory':
                        nome = n_str(data_json[t]['name({"language":"pt"})'].strip())
                        insert_sports(self, nome.encode("latin-1").decode("utf-8"), data_json[t]['slug'], data_json[t]['id'], add_ind=self.add_ind)
    #
    # def get_dados(self):
    #     self.get_all_sports()
    #     self.get_all_camp()
    #
    # def get_all_sports(self):
    #     url = 'https://sportsbet.io/pt/sports'
    #     headers = {
    #         'Host': 'sportsbet.io',
    #         'User-Agent': self.user_agent,
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    #         'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    #         #'Accept-Encoding': 'gzip, deflate, br',
    #         #'Referer': 'https://sportsbet.io/pt/sports',
    #         'Cookie': self.cookies,
    #         'Upgrade-Insecure-Requests': '1',
    #         'Sec-Fetch-Dest': 'document',
    #         'Sec-Fetch-Mode': 'navigate',
    #         'Sec-Fetch-Site': 'none',
    #         'Sec-Fetch-User': '?1',
    #     }
    #     cookies = ler_cookies()
    #     time1 = str(int(time.time()))
    #     time2 = str(int(time.time())+1)
    #     cookie_new = '_fs_tab_id=c098b7e0d6e030;__cfwaitingroom=Chh4SUdKOEIvL3A2dEpuUGZLWWpxU2RBPT0SkAJJQlBhbEJIUEFzMjNDZlVKZlQ5czZJd2tvVlM3Wk85bEpNbDloS2VPSnNkQXBKa2Fkd2Vud0Z0NTAyandtWHZlVXl1Z1Y1ODF2SXRPRW9Sd0Q2UXU5Wk9hMEVnNXZpU3dtSWJIMHBRcWgrb0NMN08xRXlVMzBRcmVlMlVMV0Fnb0YwSmNBS2l4TVpZK2d0OVRYTTg2QXI5MGtud1lEejJJR2hOa3NHN29PbFJuK1NxckZHak1kQmNvc1JRZ3FoZzZOTThySGllZElWQ2RkWHRJaUh3Y2YvOTF1R3l2TkdoNitOL1dkRVNNei9BNVAyUmF3UWtnMFJmK3dMR3ZuK3J6dmtOSURmblNIQWc0emtKNA%3D%3D; _ga_SEKFV66B0S=GS1.1.1666120922.5.0.' + time2  + '.60.0.0; _wingify_pc_uuid=fdfe2b79ad6745aea34c916a0ed6593c; __tid=uid-8271807831.2962218641; _sp_srt_id.b17c=9d06db3f-4e9a-4a76-a92c-c62010ebc888.1665845234.6.' + time1 + '.1666118246.f8b561b9-65df-4985-9a9b-b4b4950cf68d; _ga=GA1.2.1290975728.1665845236; tryMetamaskHide=true; fs_uid=#BN5B8#4935986190192640:4955098419007488:::#/1697381259; fs_cid=1.0; adformfrpid=5312976836832772683; wingify_donot_track_actions=0; g_state={"i_p":1666721925579,"i_l":3}; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; _gid=GA1.2.1016127202.1666115464; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRhYzRhNmMwNzcyMjQ4NGIxNzZhNWI=; __cf_bm=wA2ut61F1buOGqB6yH6n2RYBpR.d2E3lwhWA0bMudt8-1666120924-0-Adz1Qtsa2YQlbKzZ9U8jOCApkeh5TdgvEiZnB+qrby1PykOxoSc0AgSbeOUljC0ebquimOUToTCiuBtjtPDDDPY='
    #     cookie_new2= '_wingify_pc_uuid=fdfe2b79ad6745aea34c916a0ed6593c; __tid=uid-8271807831.2962218641; _sp_srt_id.b17c=9d06db3f-4e9a-4a76-a92c-c62010ebc888.1665845234.6.'+ time1+'.1666118246.f8b561b9-65df-4985-9a9b-b4b4950cf68d; tryMetamaskHide=true; fs_uid=#BN5B8#4935986190192640:6491650097909760:::#/1697381259; fs_cid=1.0; adformfrpid=5312976836832772683; wingify_donot_track_actions=0; g_state={"i_p":1666721925579,"i_l":3}; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; refAff=affid=148&cxid=148_390538&source=834dde61122; _ga=GA1.2.9566590343.5008065082; _gid=GA1.2.1327268174.1666120956; _ga_SEKFV66B0S=GS1.1.1666120922.5.1.' + time2 + '.59.0.0; GW_CLIENT_ID=40044fa102acb6931773f9360c70e283567eaf87ea7c4b89903a7a877fa08a4a; __cf_bm=Ln.Y1No9IXJFQpjhDKUY.WlPuJEJZtSgZ84fuOw6kvE-1666128101-0-AavS/k5pOAmxrYDj8esgJL23FzifJ7GjEgOyhW+k4fZCCbBQAMG0YpC/Kxj4hg3MHaI+ohbLrYinCwyjso54zGU=; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRhYzRhNmMwNzcyMjQ4NGIxNzZhNWI='
    #     cookie_new3 = 'experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; __cf_bm=9sbw_fRdetRON3Wjow7ly1g.J8IFlnthW9ptWMbQ8ho-1666128904-0-ATMuKJ5hzL8s134AhK3K/DPVoaRAPYB2p/hUJ+J2/ME3NDCw4rnO67waTOWgsQuNgRrMpCVfvXOfTMSn+tIG165CKjfL0SlznbiiUriwqPSXQsyuZuyKm3mCFI8l1g63uKoAhjnAb1npnOwDdPqx6otS00EA2w2Mj9csG79ylN3I; MKTSRC={"t":1666128900100,"d":{"src":"direct","mdm":"direct","cmp":"","kwd":"","cnt":"","glc":"","msc":""}}; _dd_s=rum=1&id=dc45aae9-96bb-46fe-8179-b46d2bf10706&created=1666128900587&expire=1666129925735&logs=1; _wingify_pc_uuid=c294ceb68ad8497b8289e1ef8b2d0b0e; __tid=uid-7391421832.7179433751; _ga_SEKFV66B0S=GS1.1.1666128903.1.1.1666128926.37.0.0; _ga=GA1.2.1039401276.1666128903; _sp_srt_ses.b17c=*; _sp_srt_id.b17c=42aeeb8c-d7a9-4532-91a8-937e2a30feeb.1666128903.1.1666128925.1666128903.f932475b-84a3-4a2c-85e9-e27a4bf8f5d8; GW_CLIENT_ID=90a8bb8c57052b0cd7bd6b450c43fc5cd2f8ee09d324114126c240ba5e204dc5; _gid=GA1.2.581277808.1666128908; adformfrpid=381027116410573887; fs_uid=#BN5B8#6367371768336384:5049902054215680:::#/1697664908; fs_cid=1.0; wingify_donot_track_actions=0; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRmMWMwMTY0MGNkYjZlMWZjNDM1ZWY='
    #     headersX = {'Host': 'sportsbet.io',
    #                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    #                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    #                 'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    #                 'Cookie': cookie_new3,
    #                 'Upgrade-Insecure-Requests': '1',
    #                 'Sec-Fetch-Dest': 'document',
    #                 'Sec-Fetch-Mode': 'navigate',
    #                 'Sec-Fetch-Site': 'none',
    #                 'Sec-Fetch-User': '?1'}
    #     urlf = "https://sportsbet.io/pt/sports"
    #     tester = requests.get(url=urlf, headers=headersX)
    #
    #     urlxx = "http://2captcha.com/in.php?key=0a8b7adcaded3fb07836cb56a47b111f&method=userrecaptcha&version=v3&action=verify&min_score=0.3&googlekey=6LeljvsfAAAAACR46bzAIy6Cukry12i-LpJe7U_H&pageurl=https://sportsbet.io/pt/sports"
    #     tester = self.sessao.get(url=urlxx, allow_redirects=True)
    #
    #     html_text = get_url_str(self, url=url, headers=headers).text
    #     soup = BeautifulSoup(html_text, 'html.parser')
    #     headers = {
    #         'User-Agent': self.user_agent,
    #         'Accept': '*/*',
    #         'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    #         'Referer': f'https://sportsbet.io/pt/sports/soccer/matches/future',
    #         'content-type': 'application/json',
    #         'Origin': 'https://sportsbet.io',
    #         'Sec-Fetch-Dest': 'empty',
    #         'Sec-Fetch-Mode': 'cors',
    #         'Sec-Fetch-Site': 'same-origin',
    #         'Cookie': self.cookies
    #     }
    #     data = {"operationName": "SportEventListQuery",
    #             "variables": {"language": "pt", "site": "sportsbet", "slug": 'soccer',
    #                           "timePeriod": "ANY", "leagueTournaments": "ANY", "featuredLeagueTournaments": "ANY",
    #                           "tournamentEventCount": "ANY"},
    #             "query": "query SportEventListQuery($language: String!, $slug: String!, $timePeriod: SportsbetNewGraphqlSportLeagues!, $leagueTournaments: SportsbetNewGraphqlLeagueTournaments!, $featuredLeagueTournaments: SportsbetNewGraphqlFeaturedLeagueTournaments!, $tournamentEventCount: SportsbetNewGraphqlTournamentEventCount!, $site: String) {\n  sportsbetNewGraphql {\n    id\n    getSportBySlug(slug: $slug, site: $site) {\n      id\n      slug\n      featuredLeague {\n        id\n        name(language: $language)\n        tournaments(childType: $featuredLeagueTournaments) {\n          id\n          slug\n          name(language: $language)\n          eventCount(childType: $tournamentEventCount)\n          league {\n            id\n            slug\n            name(language: $language)\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      name(language: $language)\n      leagues(childType: $timePeriod) {\n        id\n        name(language: $language)\n        slug\n        tournaments(childType: $leagueTournaments) {\n          id\n          slug\n          name(language: $language)\n          eventCount(childType: $tournamentEventCount)\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    #     response_json = post_url_str(self, url=url, headers=headers, data=data)
    #
    #     for link in soup.find_all('script'):
    #         if 'window.APOLLO_STATE=' in link.text:
    #             data = link.text
    #             start = data.find('window.APOLLO_STATE=JSON.parse("') + len('window.APOLLO_STATE=JSON.parse("')
    #             end = data.find('window.APPLICATION_CONTEXT=JSON.parse("')
    #             substring = data[start:end].strip()[:-3]
    #             data_json = json.loads(codecs.decode(substring, 'unicode_escape'))
    #             for t in data_json:
    #                 if '__typename' in data_json[t] and data_json[t]['__typename'] == 'SportsbetNewGraphqlSportCategory':
    #                     nome = data_json[t]['name({"language":"pt"})'].strip()
    #                     insert_sports(self, nome.encode("latin-1").decode("utf-8"), data_json[t]['slug'], data_json[t]['id'])
    #                     # sqlgg = f'SELECT id from ind_sports WHERE sport_name="{nomex}";'
    #                     # check_ind = self.conexao.bd(sqlgg, fetch=True)
    #                     # if check_ind:
    #                     #     sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, id_ind_sport, slug) VALUES ({self.id_site},"{id}","{nomex}", {check_ind[0][0]},"{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
    #                     # else:
    #                     #     sqlxx = f'INSERT INTO sit_sports (id_site, id_site_sport, site_sport_name, slug) VALUES ({self.id_site},"{id}","{nomex}", "{slug}") ON DUPLICATE KEY UPDATE site_sport_name="{nomex}", slug="{slug}";'
    #                     # id_bd = self.conexao.bd(sqlxx, fetch=False)
    #                     # if id_bd == 0:
    #                     #     t_id_bd = self.conexao.bd(f'SELECT id FROM sit_sports WHERE id_site = {self.id_site} and id_site_sport = "{id}"', fetch=True)
    #                     #     if t_id_bd: id_bd = t_id_bd[0][0]
    #                     # self.sports[nomex] = {'nome': nomex, 'slug': slug, 'id_bd': id_bd, 'id_site': id}
    #
    # def get_all_camp(self):
    #     url = 'https://sportsbet.io/graphql'
    #     for e in self.sports:
    #         headers = {
    #             'User-Agent': self.user_agent,
    #             'Accept': '*/*',
    #             'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    #             'Referer': f'https://sportsbet.io/pt/sports/{self.sports[e]["slug"]}/matches/future',
    #             'content-type': 'application/json',
    #             'Origin': 'https://sportsbet.io',
    #             'Sec-Fetch-Dest': 'empty',
    #             'Sec-Fetch-Mode': 'cors',
    #             'Sec-Fetch-Site': 'same-origin',
    #             'Cookie': self.cookies
    #         }
    #         data = {"operationName":"SportEventListQuery","variables":{"language":"pt","site":"sportsbet","slug": self.sports[e]['slug'],"timePeriod":"ANY","leagueTournaments":"ANY","featuredLeagueTournaments":"ANY","tournamentEventCount":"ANY"},"query":"query SportEventListQuery($language: String!, $slug: String!, $timePeriod: SportsbetNewGraphqlSportLeagues!, $leagueTournaments: SportsbetNewGraphqlLeagueTournaments!, $featuredLeagueTournaments: SportsbetNewGraphqlFeaturedLeagueTournaments!, $tournamentEventCount: SportsbetNewGraphqlTournamentEventCount!, $site: String) {\n  sportsbetNewGraphql {\n    id\n    getSportBySlug(slug: $slug, site: $site) {\n      id\n      slug\n      featuredLeague {\n        id\n        name(language: $language)\n        tournaments(childType: $featuredLeagueTournaments) {\n          id\n          slug\n          name(language: $language)\n          eventCount(childType: $tournamentEventCount)\n          league {\n            id\n            slug\n            name(language: $language)\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      name(language: $language)\n      leagues(childType: $timePeriod) {\n        id\n        name(language: $language)\n        slug\n        tournaments(childType: $leagueTournaments) {\n          id\n          slug\n          name(language: $language)\n          eventCount(childType: $tournamentEventCount)\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    #         response_json = post_url_json(url=url, headers=headers, data=data)
    #         dados = response_json['data']['sportsbetNewGraphql']['getSportBySlug']
    #         if 'featuredLeague' in dados and 'tournaments' in dados['featuredLeague']:
    #             for t in dados['featuredLeague']['tournaments']:
    #                 if 'league' in t and not t['league']['slug'] in self.paises:
    #                     insert_pais(self, t["league"]["name"].strip(), t["league"]["slug"], t["league"]["id"])
    #                     # sqlgg = f'SELECT id from ind_paises WHERE pais_name="{t["league"]["name"].strip()}";'
    #                     # check_ind = self.conexao.bd(sqlgg, fetch=True)
    #                     # if check_ind:
    #                     #     sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, id_ind_pais, slug) VALUES ({self.id_site},"{t["league"]["id"]}","{t["league"]["name"].strip()}",{check_ind[0][0]},"{t["league"]["slug"]}") ON DUPLICATE KEY UPDATE site_pais_name="{t["league"]["name"].strip()}", slug="{t["league"]["slug"]}";'
    #                     # else:
    #                     #     sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, slug) VALUES ({self.id_site},"{t["league"]["id"]}","{t["league"]["name"].strip()}","{t["league"]["slug"]}") ON DUPLICATE KEY UPDATE site_pais_name="{t["league"]["name"].strip()}", slug="{t["league"]["slug"]}";'
    #                     # id_bd = self.conexao.bd(sqlxx, fetch=False)
    #                     # if id_bd == 0:
    #                     #     t_id_bd = self.conexao.bd(f'SELECT id FROM sit_paises WHERE id_site = {self.id_site} and id_site_pais="{t["league"]["id"]}"', fetch=True)
    #                     #     if t_id_bd: id_bd = t_id_bd[0][0]
    #                     # self.paises[t["league"]["slug"]] = {'name': t["league"]["name"].strip(), 'id_bd': id_bd, 'id_site': t["league"]["id"]}
    #
    #                 if not t['slug'] in self.campeonatos:
    #                     insert_camp(self, t['name'].strip(), t['slug'], t['id'], self.sports[e], self.paises[t["league"]["slug"]])
    #
    #                     # self.campeonatos[t['slug']] = {'name': t['name'].strip(), 'id': t['id']}
    #                     # sqlxx = f'INSERT INTO sit_camp (id_site, id_site_sport, id_site_pais, id_site_camp, site_camp_name, slug) VALUES ({self.id_site}, {self.sports[e]["id_bd"]}, {self.paises[t["league"]["slug"]]["id_bd"]}, "{t["id"]}","{t["name"].strip()}","{t["slug"]}") ON DUPLICATE KEY UPDATE site_camp_name="{t["name"]}", slug="{t["slug"]}";'
    #                     # self.conexao.bd(sqlxx, fetch=False)
    #
    #         if 'leagues' in dados:
    #             for p in dados['leagues']:
    #                 if not p['slug'] in self.paises:
    #                     insert_pais(self, p["name"].strip(), p["slug"], p["id"])
    #                     # sqlgg = f'SELECT id from ind_paises WHERE pais_name="{p["name"]}";'
    #                     # check_ind = self.conexao.bd(sqlgg, fetch=True)
    #                     # if check_ind:
    #                     #     sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, id_ind_pais, slug) VALUES ({self.id_site},"{p["id"]}","{p["name"].strip()}",{check_ind[0][0]},"{p["slug"]}") ON DUPLICATE KEY UPDATE site_pais_name="{p["name"].strip()}", slug="{p["slug"]}";'
    #                     # else:
    #                     #     sqlxx = f'INSERT INTO sit_paises (id_site, id_site_pais, site_pais_name, slug) VALUES ({self.id_site},"{p["id"]}","{p["name"].strip()}","{p["slug"]}") ON DUPLICATE KEY UPDATE site_pais_name="{p["name"].strip()}", slug="{p["slug"]}";'
    #                     # id_bd = self.conexao.bd(sqlxx, fetch=False)
    #                     # if id_bd == 0:
    #                     #     t_id_bd = self.conexao.bd(f'SELECT id FROM sit_paises WHERE id_site = {self.id_site} and id_site_pais="{p["id"]}"', fetch=True)
    #                     #     if t_id_bd: id_bd = t_id_bd[0][0]
    #                     # self.paises[p["slug"]] = {'name': p["name"].strip(), 'id_bd': id_bd, 'id_site': p["id"]}
    #                 for t in p['tournaments']:
    #                     if not t['slug'] in self.campeonatos and t['name'] != None:
    #                         insert_camp(self, t['name'].strip(), t['slug'], t['id'], self.sports[e], self.paises[p["slug"]])
    #                         # self.campeonatos[t['slug']] = {'name': t['name'].strip(), 'id': t['id']}
    #                         # sqlxx = f'INSERT INTO sit_camp (id_site, id_site_sport, id_site_pais, id_site_camp, site_camp_name, slug) VALUES ({self.id_site},{self.sports[e]["id_bd"]}, {self.paises[p["slug"]]["id_bd"]}, "{t["id"]}","{t["name"].strip()}","{t["slug"]}") ON DUPLICATE KEY UPDATE site_camp_name="{t["name"].strip()}", slug="{t["slug"]}";'
    #                         # self.conexao.bd(sqlxx, fetch=False)
    #         xxx = 0
    #         # for e in response_json['data']:
    #         #     for e1 in response_json['data'][e]:
    #         #         xx = response_json['data'][e][e1]
    #         #         xxx = 0
    #         #
