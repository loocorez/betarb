import time

import undetected_chromedriver.v2 as uc
from time import sleep
from random import randint
import asyncio
import requests
# driver = uc.Chrome()
# driver.get('https://www.sportsbet.io')
# driver.maximize_window()

import json
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from apify_client import ApifyClient

import urllib.request
import json

datapost = {"operationName":"IsBlockedQuery","variables":{"site":"sportsbet"},"query":"query IsBlockedQuery($site: String) {\n  __typename\n  userManagement {\n    id\n    __typename\n    currentCountryInfo(site: $site) {\n      id\n      __typename\n      countryCode\n      blocked\n    }\n  }\n}\n"}
req = urllib.request.Request("https://sportsbet.io/graphql")
req.set_proxy('localhost:12960', 'http')
jsondataasbytes = json.dumps(datapost).encode('utf-8')
req.add_header('Host', 'sportsbet.io')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0')
req.add_header('Accept', '*/*')
req.add_header('Accept-Language', 'pt-BR')
req.add_header('Accept-Encoding', 'gzip, deflate, br')
req.add_header('Referer', 'https://sportsbet.io/pt/sports/soccer/matches')
req.add_header('content-type', 'application/json')
req.add_header('authorization', '')
req.add_header('Content-Length', len(jsondataasbytes))
req.add_header('Origin', 'https://sportsbet.io')
req.add_header('Connection', 'keep-alive')
req.add_header('Cookie', 'experiments=%7B%22arLUC_zhRlKw0HignXgxRA%22%3A3%7D; __cf_bm=UjQaM3bZQr1Q.3KQ9OU031eGonKHtRAmH_7.xGzMtZU-1666931562-0-AZvkc8AMAoiR+yMHQC6RdVQOSUfMDx7r7VZOAX1+L0WVh0go5dVxpJksthxnU1wlGgLTps6pk+JHctnh+Y7ux8O05MVT2l1jwR8fVIIvyLpZNGap28Pp0HWQKmrCgoBJbtYZ3VwzefkbAgytjWc9pvzc4VEB/cjVspiTjW8o+ILZ; MKTSRC={"t":1666931556047,"d":{"src":"direct","mdm":"direct","cmp":"","kwd":"","cnt":"","glc":"","msc":""}}; _dd_s=rum=1&id=445f552e-d35d-4f62-9a20-016cdd9d995d&created=1666931556409&expire=1666933296531&logs=1; _wingify_pc_uuid=3c2e72de441746b3b18fc80346541c02; _ga=GA1.1.1319834409.1666931557; _gid=GA1.2.660195486.1666931557; _sp_srt_ses.b17c=*; _sp_srt_id.b17c=908d6597-2141-44fe-996d-61e086a1ccc3.1666931557.1.1666931559.1666931557.df1de284-870c-4483-ae76-34517b9b3d86; _gaexp=GAX1.2.MQqvV8zHTwySZnml_3meAA.19385.1; adformfrpid=7430061673401368091; _ga_SEKFV66B0S=GS1.1.1666931558.1.0.1666931558.60.0.0; GW_CLIENT_ID=4d41a7ad047e241848f1fd63637c17ad99586e63da630b3af6be3ac7ca7a13a6; fs_uid=#BN5B8#6458898589437952:5797424624848896:::#/1698467562; fs_cid=1.0; wingify_donot_track_actions=0; userPreferenceId=U3BvcnRzYmV0UHJlZmVyZW5jZXNVc2VyUHJlZmVyZW5jZTo2MzViNWI2NDEyNjlkOTFmZDI4N2Y5NTE=')
req.add_header('Sec-Fetch-Dest', 'empty')
req.add_header('Sec-Fetch-Mode', 'cors')
req.add_header('Sec-Fetch-Site', 'same-origin')
  # needs to be bytes
response = urllib.request.urlopen(req, jsondataasbytes)




import urllib.request
import json
reqUrl = 'https://randomuser.me/api/'
reqData = None
headers = {
    'Content-Type': 'application/json'
}
method = 'POST'
proxy_host = 'localhost:12960'    # host and port of your proxy
url = 'https://jsonplaceholder.typicode.com/posts/'

req = request.Request(reqUrl, reqData, headers, method=method)
req.set_proxy(proxy_host, 'http')
req = request.Request(reqUrl, reqData, headers, method=method)
with request.urlopen(req) as res:
  body = json.load(res)
  print(body)

def get_async_data(route, request):
    method = 'POST'
    postData = {"operationName":"SportQuery","variables":{"language":"pt","site":"sportsbet","slug":"soccer"},"query":"query SportQuery($language: String!, $slug: String!, $site: String) {\n  sportsbetNewGraphql {\n    id\n    getSportBySlug(slug: $slug, site: $site) {\n      id\n      slug\n      name(language: $language)\n      enName: name(language: \"en\")\n      iconCode\n      liveEventCount: eventCount(childType: LIVE)\n      todayEventCount: eventCount(childType: TODAY)\n      futureEventCount: eventCount(childType: ANY)\n      leagues(childType: ANY) {\n        id\n        tournaments(childType: ANY) {\n          id\n          events(childType: ANY, first: 1) {\n            id\n            information {\n              provider_prefix\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    responseX = route.continue_(method, postData)
    print(responseX)
    xxx = 0



async def main():
    launchOptionsX = proxy = {
        "server": '127.0.0.1:12960'  # ,
        # 'username': 'My_user',
        # "password": 'My_password',
    }


    async with async_playwright() as p:
        # browser = await p.firefox.launch(
        #     headless=False,
        #     devtools=True,
        #     proxy=launchOptionsX,
        # )
        url = "https://sportsbet.io"
        path = '/pt/sports'
        # url = "https://bet365.com"
        # path = '/'

        browser = await p.firefox.launch(headless=False, proxy=launchOptionsX)
        context = await browser.new_context(base_url=url, ignore_https_errors=True)

        page = await context.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 870})
        await page.goto(path, wait_until="domcontentloaded", )
        await asyncio.sleep(10)
        await page.locator('footer').is_enabled()
        #locatorxx = page.locator('tag=footer >> className="FooterContainer-sc-18uurvk-0 bUOomo"').first
        # page.on("response", lambda response: print("<<", response.headers, response.url))
        #await page.screenshot(path="sportsbet.png")
        # cookies = context.cookies()
        cookies = await context.cookies()
        string_cookies = ''
        for c in cookies:
            if c['domain'] == '.sportsbet.io' or c['domain'] == 'sportsbet.io':
                string_cookies += f"{c['name']}={c['value']};"
        headers = {
            'Accept': '*/*',
            'Host': 'sportsbet.io',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://sportsbet.io/pt/sports',
            'content-type': 'application/json',
            'Origin': 'https://sportsbet.io',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cookie': string_cookies,
        }
        datapost = {"operationName": "SportQuery",
                    "variables": {"language": "pt", "site": "sportsbet", "slug": "soccer"},
                    "query": "query SportQuery($language: String!, $slug: String!, $site: String) {\n  sportsbetNewGraphql {\n    id\n    getSportBySlug(slug: $slug, site: $site) {\n      id\n      slug\n      name(language: $language)\n      enName: name(language: \"en\")\n      iconCode\n      liveEventCount: eventCount(childType: LIVE)\n      todayEventCount: eventCount(childType: TODAY)\n      futureEventCount: eventCount(childType: ANY)\n      leagues(childType: ANY) {\n        id\n        tournaments(childType: ANY) {\n          id\n          events(childType: ANY, first: 1) {\n            id\n            information {\n              provider_prefix\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}



        contextP = await browser.new_context(base_url=url, ignore_https_errors=True, extra_http_headers=headers)
        post_context = contextP.request
        response = await post_context.post("/graphql", data=datapost)
        cookies2 = await context.cookies()
        url2 = url+"/graphql"
        responsea = requests.post(url=url2, json=datapost, headers=headers)
        headers2 = {
            'Accept': '*/*',
            'Host': 'sportsbet.io',
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://sportsbet.io/pt/sports',
            'content-type': 'application/json',
            'Origin': 'https://sportsbet.io',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            #'Cookie': string_cookies,
        }
        testepost = context.request
        time.sleep(5)
        response2 = await testepost.post("/graphql", data=datapost, headers=headers2)
        teste = await response2.text()
        injected_javascript = (
            'const time = Date.now();'
            'const callback = arguments[0];'
            'const handleDocumentLoaded = () => {'
            '  document.getElementById("injected-time").innerHTML = time;'
            '  callback();'
            '};'
            'if (document.readyState === "loading") {'
            '  document.addEventListener("DOMContentLoaded", handleDocumentLoaded);'
            '} else {'
            '  handleDocumentLoaded();'
            '}'
        )
        url = await page.evaluate(f'<script>{injected_javascript}</script>alert()')
        await page.route('/graphql/', get_async_data)
        while True:
            await asyncio.sleep(30)
        # page.on('requestfinished', local_request_finished_info)

        # await page.goto('https://www.facebook.com/twdaynews', timeout=300000)
        # await page.wait_for_load_state('load', timeout=300)
        #print(f'title:{await page.title()}')

asyncio.run(main())
while True:
    time.sleep(5)

def get_sync_data(route, request):
    method = 'POST'
    postData = {"operationName":"SportQuery","variables":{"language":"pt","site":"sportsbet","slug":"soccer"},"query":"query SportQuery($language: String!, $slug: String!, $site: String) {\n  sportsbetNewGraphql {\n    id\n    getSportBySlug(slug: $slug, site: $site) {\n      id\n      slug\n      name(language: $language)\n      enName: name(language: \"en\")\n      iconCode\n      liveEventCount: eventCount(childType: LIVE)\n      todayEventCount: eventCount(childType: TODAY)\n      futureEventCount: eventCount(childType: ANY)\n      leagues(childType: ANY) {\n        id\n        tournaments(childType: ANY) {\n          id\n          events(childType: ANY, first: 1) {\n            id\n            information {\n              provider_prefix\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    route.continue_(method, postData)

launchOptionsX = proxy={
        "server": '127.0.0.1:12960'#,
        # 'username': 'My_user',
        # "password": 'My_password',
    }
with sync_playwright() as p:
    browser = p.firefox.launch(headless=False, proxy=launchOptionsX)

    # page = browser.new_page()
    # page.goto('https://sportsbet.io', wait_until="commit")

    # context = browser.new_context(base_url="https://stake.com")
    # page = context.new_page()
    # page.goto('/', wait_until="networkidle", )
    # locator = page.locator("footer").first
    # locatorxx = page.locator('tag=div >> className="container svelte-x7f9v0"').first
    # page.screenshot(path="stake.png")



    context = browser.new_context(base_url="https://sportsbet.io", ignore_https_errors=True)
    page = context.new_page()
    page.set_viewport_size({'width': 1920, 'height': 870})
    page.goto('/pt/sports', wait_until="domcontentloaded", )
    #wait_for_selector
    locatorxx = page.locator('tag=footer >> className="FooterContainer-sc-18uurvk-0 bUOomo"').first
    #page.on("response", lambda response: print("<<", response.headers, response.url))
    page.screenshot(path="sportsbet.png")
    cookies = context.cookies()

    response = page.route('/api/graphql/', get_sync_data)

    string_cookies = ''
    for c in cookies:
        if c['domain'] == '.sportsbet.io':
            string_cookies += f"{c['name']}={c['value']};"
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://sportsbet.io/pt/sports/soccer/inplay',
        'content-type': 'application/json',
        'Origin': 'https://sportsbet.io',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cookie': string_cookies
    }
    datapost = {"operationName":"SportQuery","variables":{"language":"pt","site":"sportsbet","slug":"soccer"},"query":"query SportQuery($language: String!, $slug: String!, $site: String) {\n  sportsbetNewGraphql {\n    id\n    getSportBySlug(slug: $slug, site: $site) {\n      id\n      slug\n      name(language: $language)\n      enName: name(language: \"en\")\n      iconCode\n      liveEventCount: eventCount(childType: LIVE)\n      todayEventCount: eventCount(childType: TODAY)\n      futureEventCount: eventCount(childType: ANY)\n      leagues(childType: ANY) {\n        id\n        tournaments(childType: ANY) {\n          id\n          events(childType: ANY, first: 1) {\n            id\n            information {\n              provider_prefix\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    response = context.request.post("/graphql", headers=headers, data=datapost)
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