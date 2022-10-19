import time

import undetected_chromedriver.v2 as uc
from time import sleep
from random import randint


# driver = uc.Chrome()
# driver.get('https://www.sportsbet.io')
# driver.maximize_window()

import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    # page = browser.new_page()
    # page.goto('https://sportsbet.io', wait_until="commit")

    # context = browser.new_context(base_url="https://bet365.com")
    # api_request_context = context.request
    # page = context.new_page()
    # page.goto('/#/AS/B1/', wait_until="domcontentloaded", )
    # time.sleep(20)
    # #page.innerHTML('Stake.com - ')
    # # page.on("response", lambda response: print("<<", response.headers, response.url))
    # page.screenshot(path="bet365.png")


    context = browser.new_context(base_url="https://sportsbet.io")
    api_request_context = context.request
    page = context.new_page()
    page.goto('/pt/sports',wait_until="load", )
    #page.on("response", lambda response: print("<<", response.headers, response.url))
    page.screenshot(path="teste.png")
    cookies = context.cookies()

    string_cookies = ''
    for c in cookies:
        if c['domain'] == '.sportsbet.io':
            string_cookies += f"{c['name']}={c['value']};"
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://sportsbet.io/pt/sports',
        'content-type': 'application/json',
        'Origin': 'https://sportsbet.io',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cookie': string_cookies
    }
    datapost = {"operationName":"DesktopEuropeanEventListPreviewQuery","variables":{"language":"pt","site":"sportsbet","tournamentId":"U3BvcnRzYmV0TmV3R3JhcGhxbFRvdXJuYW1lbnQ6NjA2NmMxMmI3MDMwMWM1ZTQyMTBiNTlj","childType":"LIVE","cricketIncluded":'false'},"query":"query DesktopEuropeanEventListPreviewQuery($language: String!, $tournamentId: GraphqlId!, $childType: SportsbetNewGraphqlTournamentEvents!, $cricketIncluded: Boolean!) {\n  sportsbetNewGraphql {\n    id\n    getTournamentById(id: $tournamentId) {\n      id\n      events(childType: $childType) {\n        ...DesktopEuropeanEventFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment DesktopEuropeanEventFragment on SportsbetNewGraphqlEvent {\n  id\n  __typename\n  asian {\n    id\n    __typename\n    ftMatchWinner {\n      ...EventListMarketQueryFragment\n      __typename\n    }\n    ftTotal {\n      ...EventListMarketQueryFragment\n      __typename\n    }\n    ftHandicap {\n      ...EventListMarketQueryFragment\n      __typename\n    }\n  }\n  ...EventListInformationQueryFragment\n}\n\nfragment EventListMarketQueryFragment on SportsbetNewGraphqlMarket {\n  id\n  __typename\n  enName: name(language: \"en\")\n  name(language: \"en\")\n  status\n  specifiers\n  selections {\n    id\n    __typename\n    enName: name(language: \"en\")\n    name(language: $language)\n    active\n    odds\n    providerProductId\n  }\n  market_type {\n    id\n    __typename\n    name\n    description\n    translation_key\n    type\n    settings {\n      id\n      betBoostMultiplier\n      __typename\n    }\n  }\n}\n\nfragment EventListInformationQueryFragment on SportsbetNewGraphqlEvent {\n  id\n  __typename\n  type\n  status\n  start_time\n  market_count\n  live_odds\n  slug\n  name(language: $language)\n  enName: name(language: \"en\")\n  maxBetAvailable\n  videoStream {\n    id\n    __typename\n    streamAvailable\n  }\n  sport {\n    id\n    __typename\n    slug\n    name(language: $language)\n    betBoostMultiplier\n    iconCode\n  }\n  league {\n    id\n    __typename\n    slug\n    name(language: $language)\n    betBoostMultiplier\n  }\n  tournament {\n    id\n    __typename\n    slug\n    name(language: $language)\n    betBoostMultiplier\n  }\n  competitors {\n    id\n    __typename\n    name\n    type\n    betradarId\n  }\n  information {\n    id\n    __typename\n    match_time\n    provider_prefix\n    period_scores {\n      id\n      __typename\n      home_score\n      away_score\n    }\n    match_status_translations(language: $language)\n    home_score\n    away_score\n    home_gamescore\n    away_gamescore\n    provider_product_id\n  }\n  premiumCricketScoringData @include(if: $cricketIncluded) {\n    ...CricketStatsFragment\n    __typename\n  }\n  isSportcastFixtureActive\n  sportcastFixtureId\n}\n\nfragment CricketStatsFragment on SportsbetNewGraphqlPremiumCricketScore {\n  id\n  matchTitle\n  matchCommentary\n  battingTeam {\n    id\n    teamWickets\n    teamRuns\n    teamOvers\n    teamName\n    sixes\n    fours\n    extras\n    competitorId\n    __typename\n  }\n  previousInnings {\n    id\n    wickets\n    teamName\n    summary\n    runs\n    oversAvailable\n    overs\n    inningsNumber\n    conclusion\n    competitorId\n    __typename\n  }\n  overs {\n    id\n    runs\n    overNumber\n    isCurrentOver\n    balls\n    __typename\n  }\n  batsmen {\n    sixes\n    runs\n    onStrike\n    fours\n    batsmanName\n    balls\n    active\n    __typename\n  }\n  __typename\n}\n"}
    response = api_request_context.post("/graphql", headers=headers, data=datapost)
    teste = page.innerHTML()
    ua = page.query_selector(".user-agent")
    ua.inner_html()
    jsonContent = json.loads(page.inner_text('pre'))
    print(jsonContent['headers']['User-Agent'])
    browser.close()


    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto('https://httpbin.org/headers') #, wait_until="load")
        page.screenshot(path="teste.png")
        teste = page.inner_text()
        jsonContent = json.loads(page.inner_text('pre'))
        print(jsonContent['headers']['User-Agent'])
        browser.close()

    #
# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = uc.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)