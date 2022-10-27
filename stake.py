from acessos import *
from bs4 import BeautifulSoup
import codecs, json, time
from playwright.sync_api import sync_playwright
class c_stake:
    def __init__(self, conexao):
        self.sessao = requests.session()
        self.id_site = 4
        self.mysql_conn = conexao
        #self.cookies = '__cfwaitingroom=Chh4SUdKOEIvL3A2dEpuUGZLWWpxU2RBPT0SkAJJQlBhbEJIUEFzMjNDZlVKZlQ5czZJd2tvVlM3Wk85bEpNbDloS2VPSnNkQXBKa2Fkd2Vud0Z0NTAyandtWHZlVXl1Z1Y1ODF2SXRPRW9Sd0Q2UXU5Wk9hMEVnNXZpU3dtSWJIMHBRcWgrb0NMN08xRXlVMzBRcmVlMlVMV0Fnb0YwSmNBS2l4TVpZK2d0OVRYTTg2QXI5MGtud1lEejJJR2hOa3NHN29PbFJuK1NxckZHak1kQmNvc1JRZ3FoZzZOTThySGllZElWQ2RkWHRJaUh3Y2YvOTF1R3l2TkdoNitOL1dkRVNNei9BNVAyUmF3UWtnMFJmK3dMR3ZuK3J6dmtOSURmblNIQWc0emtKNA%3D%3D; _ga_SEKFV66B0S=GS1.1.1666120922.5.0.1666120922.60.0.0; _wingify_pc_uuid=fdfe2b79ad6745aea34c916a0ed6593c; __tid=uid-8271807831.2962218641; _sp_srt_id.b17c=9d06db3f-4e9a-4a76-a92c-c62010ebc888.1665845234.5.1666118246.1666115462.6cd15c9f-79ea-4ace-b908-954a36708154; _ga=GA1.2.1290975728.1665845236; tryMetamaskHide=true; fs_uid=#BN5B8#4935986190192640:4955098419007488:::#/1697381259; fs_cid=1.0; adformfrpid=5312976836832772683; wingify_donot_track_actions=0; g_state={"i_p":1666721925579,"i_l":3}; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; _gid=GA1.2.1016127202.1666115464; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzRhYzRhNmMwNzcyMjQ4NGIxNzZhNWI=; __cf_bm=wA2ut61F1buOGqB6yH6n2RYBpR.d2E3lwhWA0bMudt8-1666120924-0-Adz1Qtsa2YQlbKzZ9U8jOCApkeh5TdgvEiZnB+qrby1PykOxoSc0AgSbeOUljC0ebquimOUToTCiuBtjtPDDDPY='
        #self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
        self.sports = {}
        self.paises = {}
        self.campeonatos = {}
        self.proxy = {'server': '127.0.0.1:12960'}
        self.p = sync_playwright().start()
        self.browser = self.p.firefox.launch(headless=False, proxy=self.proxy)
        self.context = self.browser.new_context(base_url="https://stake.com", ignore_https_errors=True, locale="pt-BR")
        self.page = self.context.new_page()
        self.first_acess()
        self.get_data()
    def get_data(self):
        for sport in self.sports:
            datapost = {"query":"query SportIndex($sport: String!, $group: String!, $type: SportSearchEnum = popular) {\n  slugSport(sport: $sport) {\n    id\n    name\n    templates(group: $group) {\n      id\n      name\n      extId\n    }\n    firstTournament: tournamentList(type: $type, limit: 1) {\n      id\n      name\n      fixtureCount(type: $type)\n      fixtureList(type: $type, limit: 10) {\n        ...FixturePreview\n        groups(groups: [$group], status: [active, suspended, deactivated]) {\n          ...SportGroupTemplates\n        }\n      }\n    }\n    tournamentList(type: $type, limit: 5) {\n      id\n      name\n      slug\n      fixtureCount(type: $type)\n      category {\n        id\n        slug\n        name\n      }\n    }\n    categoryList(type: $type, limit: 1000) {\n      id\n      slug\n      name\n      fixtureCount(type: $type)\n      tournamentList(type: $type, limit: 1000) {\n        id\n        slug\n        name\n        fixtureCount(type: $type)\n      }\n    }\n  }\n}\n\nfragment FixturePreview on SportFixture {\n  id\n  ...SportFixtureLiveStreamExists\n  status\n  slug\n  marketCount(status: [active, suspended])\n  extId\n  data {\n    __typename\n    ...SportFixtureDataMatch\n    ...SportFixtureDataOutright\n  }\n  tournament {\n    ...TournamentTreeNested\n  }\n  eventStatus {\n    ...SportFixtureEventStatus\n  }\n}\n\nfragment SportFixtureLiveStreamExists on SportFixture {\n  id\n  betradarStream {\n    exists\n  }\n  imgArenaStream {\n    exists\n  }\n  abiosStream {\n    exists\n    stream {\n      startTime\n      id\n    }\n  }\n  geniussportsStream(deliveryType: hls) {\n    exists\n  }\n}\n\nfragment SportFixtureDataMatch on SportFixtureDataMatch {\n  startTime\n  competitors {\n    ...SportFixtureCompetitor\n  }\n  __typename\n}\n\nfragment SportFixtureCompetitor on SportFixtureCompetitor {\n  name\n  extId\n  countryCode\n  abbreviation\n}\n\nfragment SportFixtureDataOutright on SportFixtureDataOutright {\n  name\n  startTime\n  endTime\n  __typename\n}\n\nfragment TournamentTreeNested on SportTournament {\n  id\n  name\n  slug\n  category {\n    ...CategoryTreeNested\n  }\n}\n\nfragment CategoryTreeNested on SportCategory {\n  id\n  name\n  slug\n  sport {\n    id\n    name\n    slug\n  }\n}\n\nfragment SportFixtureEventStatus on SportFixtureEventStatus {\n  homeScore\n  awayScore\n  matchStatus\n  clock {\n    matchTime\n    remainingTime\n  }\n  periodScores {\n    homeScore\n    awayScore\n    matchStatus\n  }\n  currentServer {\n    extId\n  }\n  homeGameScore\n  awayGameScore\n  statistic {\n    yellowCards {\n      away\n      home\n    }\n    redCards {\n      away\n      home\n    }\n    corners {\n      home\n      away\n    }\n  }\n}\n\nfragment SportGroupTemplates on SportGroup {\n  ...SportGroup\n  templates(limit: 3, includeEmpty: true) {\n    ...SportGroupTemplate\n    markets(limit: 1) {\n      ...SportMarket\n      outcomes {\n        ...SportMarketOutcome\n      }\n    }\n  }\n}\n\nfragment SportGroup on SportGroup {\n  name\n  translation\n  rank\n}\n\nfragment SportGroupTemplate on SportGroupTemplate {\n  extId\n  rank\n  name\n}\n\nfragment SportMarket on SportMarket {\n  id\n  name\n  status\n  extId\n  specifiers\n  customBetAvailable\n}\n\nfragment SportMarketOutcome on SportMarketOutcome {\n  active\n  id\n  odds\n  name\n  customBetAvailable\n}\n","variables":{"sport":"soccer","group":"winner"}}
            headers = {"Referer": f"https://stake.com/sports/soccer",
                       "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                       "Origin": "https://stake.com",
                       "x-forwarded-for": "187.19.130.235, 162.158.38.16, 172.20.241.65",
                       "cf-device-type":"",
                       "cf-ipcountry": "BR",
                       "Sec-Fetch-Dest": "empty",
                       "Sec-Fetch-Mode": "cors",
                       "Sec-Fetch-Site": "same-origin",
                       "x-language": "br"
            }
            retorno = self.post_data(datapost, headers)
            if retorno != None:
                    xxx = 0

    def post_data(self, datapost, headers):
        try:
            testepost = self.context.request
            response = testepost.post("/_api/graphql", data=datapost, timeout=0, headers=headers).text()
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