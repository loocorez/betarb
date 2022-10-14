import requests, json
from concurrent.futures import ThreadPoolExecutor
from acessos import *


class c_sportsbet:
    def __init__(self, conexao):
        self.id_site = 2
        self.all_campeonatos = {}
        self.conexao = conexao

    def get_all_campeonatos(self):

        #url = "https://sportsbet.io/graphql"
        # data = {"operationName":"MainMarketsQuery","variables":{"language":"pt","site":"sportsbet","eventId":"RXZlbnQ6NjMzOGFhYjFmMzBmYjk0NjE5ZTlhNWM4"},"query":"query MainMarketsQuery($eventId: GraphqlId!, $language: String!) {\n  sportsbetNewGraphql {\n    id\n    getEventById(id: $eventId) {\n      id\n      type\n      name(language: \"en\")\n      sport {\n        id\n        name(language: \"en\")\n        __typename\n      }\n      tournament {\n        id\n        name(language: \"en\")\n        __typename\n      }\n      competitors {\n        name\n        id\n        __typename\n      }\n      mainMarkets {\n        ...MainEventMarketFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MainEventMarketFragment on SportsbetNewGraphqlMarket {\n  id\n  __typename\n  name(language: $language)\n  englishName: name(language: \"en\")\n  enName: name(language: \"en\")\n  status\n  selections {\n    ...ListEventMarketSelectionFragment\n    __typename\n  }\n  market_type {\n    id\n    __typename\n    name\n    description\n    translation_key\n    type\n    settings {\n      id\n      betBoostMultiplier\n      __typename\n    }\n  }\n  specifiers\n}\n\nfragment ListEventMarketSelectionFragment on SportsbetNewGraphqlMarketSelection {\n  id\n  __typename\n  name(language: $language)\n  enName: name(language: \"en\")\n  active\n  odds\n  probabilities\n  providerProductId\n  __typename\n}\n"}
        url = 'https://sportsbet.io/pt/sports'
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
            'Cookie': 'cf_clearance=F3tN2Z0fRwmXhidsEEFfj0UfWUPJG8JyDq_NvYlPxko-1665760653-0-150; experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; _sp_srt_id.b17c=32c3e070-6bae-4713-98e6-9e7f6539d7d6.1665694911.3.1665761526.1665705765.c833aa86-7f95-488f-93be-fd51cdb7dc33; _wingify_pc_uuid=de100dd0ac4145e08977f201d9bda149; __tid=uid-7786973412.8842922656; _ga_SEKFV66B0S=GS1.1.1665760652.3.1.1665761527.60.0.0; _ga=GA1.2.1810921942.1665694912; tryMetamaskHide=true; adformfrpid=3498136337046941869; fs_uid=#BN5B8#5845328798126080:5879319565668352:::#/1697230917; fs_cid=1.0; _gid=GA1.2.653885333.1665694939; wingify_donot_track_actions=0; g_state={"i_p":1665846974149,"i_l":2}; __cf_bm=S7WYbomLfZG86cxUC7DEDUQVoMunJuz5wZAASEfIgSQ-1665761489-0-ARnZ499pjlYkFWn0nuySHtzAEDTqlJsqc4flMtK0S85X4QxqF+BWr75G3SRZfCq259bg0LVb2TSKe0ABlD5N+297WEWCpwpv6SWOmY0/VwOg51lwRvHjhiMpCU6v5ydju3YjPRyIT8Za4/yGNOCB7y6r+hgwf74hZ05bW/yFiGYO; _dd_s=rum=1&id=30ddfe2e-c9d0-4099-b39a-57f5fba2fb00&created=1665760623504&expire=1665762749677&logs=1; cf_chl_2=02781ef6b15d746; cf_chl_prog=x14; MKTSRC={"t":1665761124541,"d":{"src":"direct","mdm":"direct","cmp":"direct","kwd":"","cnt":"","gc":"","msc":""}}; GW_CLIENT_ID=b94a45ca547607ab31dcbc33502e7ae1ef0479ee9e49cc060d785d182752cf42; _sp_srt_ses.b17c=*; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzQ4N2NiYzU0ZmExYzgyZjBiNGMxNGQ='
        }
        data = get_url(url=url, headers=headers)
        xxx = 0