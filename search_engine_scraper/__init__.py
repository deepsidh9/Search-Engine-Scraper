import os
import time
import random
import requests
import urllib
import pkg_resources
import traceback
from lxml import html
from lxml.html import fromstring
from itertools import cycle

# PROXY_PATH = "proxies.txt"
PROXY_USAGE_TIMEOUT = 900
# proxies = pkg_resources.resource_stream(__name__, 'search_engine_scraper/proxies.txt')
# user_agents_file = pkg_resources.resource_stream(__name__, 'search_engine_scraper/user_agents.txt')
PROXY_PATH = os.path.join(os.path.dirname(__file__),'proxies.txt')
user_agents_file = os.path.join(os.path.dirname(__file__),'user_agents.txt')

class search_engine: 

    def __init__(self,serving_engine):
        self.serve_engine=serving_engine

    def query_encoding(self,query):
        pass
    def result_parsing(self,page):
        pass
    def search(self,query):
        pass

class serving_engine:

    def proxy_scrape(self):
        pass
    def proxy_check(self):
        pass
    def load_user_agents(self,uafile):
        pass
    def get_page(self,url):
        pass

class serve_search_engines(serving_engine):

    def __init__(self):
        self.proxy_pool = []
        self.proxy_check()
        self.user_agents = self.load_user_agents(uafile=user_agents_file)

    def proxy_scrape(self):
        """
        Returns a list of free proxies
)
        """
        print("Getting new live proxies")
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:20]:
            # if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')
                              [0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
        # return proxies
        # proxies=[]
        print("Obtained proxied are as : ", proxies)
        proxy_pool = cycle(proxies)
        proxy_list = [proxy for proxy in proxies]
        return proxy_pool, proxy_list

    def proxy_check(self):
        """
        query:string

        Checks if the old proxy pool is no older than 15 minutes, if so
        it fetches 20 new proxies and writes them to a file with the
        current time stamp

        """

        with open(PROXY_PATH) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        self.old_proxy_time = float(content[-1])
        print("The time recorded in the file is : ", self.old_proxy_time)

        self.new_proxy_time = time.time()
        print("The time now  is : ", self.new_proxy_time)

        self.time_difference = self.new_proxy_time-self.old_proxy_time
        print("A total difference of {} minutes".
              format(self.time_difference/60))

        if self.time_difference >= PROXY_USAGE_TIMEOUT:  # Setting threshold at 15 minutes
            print("It has been 15 minutes since the proxy renewal, \
                                therefore now getting New Proxies")
            self.proxy_pool, proxy_list = self.proxy_scrape()

            print("Writing the new proxies to the 'proxies.txt' file")
            with open(PROXY_PATH, 'w+') as f:  # writing proxies to list
                for proxy in proxy_list:
                    f.write("{}\n".format(proxy))
            with open(PROXY_PATH, 'a+') as f:  # writing the timestamp for referenced list
                f.write("{}\n".format(time.time()))
            print("proxy file timestamp updated")
        else:
            print("It has been less than 15 minutes since the proxies were renewed, therefore sticking with the old proxies")
            self.proxy_pool = cycle(content[:-1])

    def load_user_agents(self,uafile):
        """
        uafile : string
          path to text file of user agents, one per line
        """
        uas = []

        with open(uafile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    uas.append(ua.strip()[1:-1-1])
        random.shuffle(uas)
        return uas
    def get_page(self, url):
        """
        url:string

        'Gets' the specified URL through requests
        Checks if proxies are being used for 15 minutes, if so it fetches 20 new proxies    
        proxy_pool provides a pool of proxies through which requests are to be made

        """
        self.new_proxy_time = time.time()
        if self.new_proxy_time-self.old_proxy_time >= PROXY_USAGE_TIMEOUT:
            print("It has been more than or equal to 15 minutes since the proxy"
                    "renewal, therefore now getting New Proxies")
            self.proxy_check()
        else:
            print("Less than 15 minutes since the proxies were renewed, \
            therefore sticking with the old proxies")
            self.proxy_pool = self.proxy_pool

        # Get a proxy from the pool
        for i in range(1, 21):
            try:
                proxy = next(self.proxy_pool)
                print("Request #%d" % i)
                ua = random.choice(self.user_agents)  # select a random user agent
                print("Selected {} as the user agent".format(ua))
                print("The proxy is : {}".format(proxy))
                headers = {
                    "Connection": "close",  # another way to cover tracks
                    "User-Agent": ua}
                # page = requests.get(
                #     url, proxies={"http": proxy}, headers=headers)
                page = requests.get(
                    url, headers=headers)
                # print(page)
                # if selected_search_engine=="google":
                if page.status_code == 200:
                    break
            except Exception as exp:
                # Most free proxies will often get connection errors,
                # therefore will have to retry the entire request using another proxy to work.
                # We will just skip retries
                print("Skipping. Connnection error DUE TO :", exp)
                page= "<html>"
            print("PAGE OBJECT IS ",page)
        return page

server=serve_search_engines()

class google(search_engine):

    def __init__(self,serving_engine):
        super(google, self).__init__(server)

    def text_query_encoding(self,query):
        """
        query : string
        Query to be made through google search

        Encodes the URL as needed by google for the query to be valid
        """
        # https://www.google.com/search?tbm=isch&q=findSomeImage google images url
        url = 'https://www.google.com/search?q=' + \
            urllib.parse.quote_plus(query)  # check live debug
        print("'{}' generated as the query url".format(url))
        return url

    def text_result_parsing(self,page):
        """
        page: <class 'requests.models.Response'>
                returned object through requests after querying google.com

        Parses the page and gets the required links

        """
        tree = html.fromstring(page.content)
        # links = tree.xpath("//div[contains(@class, 'kCrYT')]/a/@href")
        links = tree.xpath("//div[contains(@class, 'r')]/a/@href")

        final_links = []
        for link in links:
            if not link.startswith('/search?'):
                if link.startswith('/url?'):
                    link = link[7:]
                    final_links.append(link)
                elif link.startswith('http'):
                    final_links.append(link)
        return final_links
    
    def search(self, query):
        """
        query:string

        Queries google for the specified query

        """
        print("""Initiating search for "{}" """.format(query))
        url = self.text_query_encoding(query)

        print("Getting the page")
        # page = self.get_page(url,proxy_pool=proxies)
        page = self.serve_engine.get_page(url)

        print("Parsing the results")
        links = self.text_result_parsing(page)
        print("LINKS ARE",links)

        print("""The search for "{}" results is now over.""".format(query))

        return links

class yahoo(search_engine):

    def __init__(self,serving_engine):
        super(yahoo, self).__init__(server)

    def text_query_encoding(self,query,country_code='in'):
        """
        query : string
        Query to be made through yahoo search

        Encodes the URL as needed by yahoo for the query to be valid
        """
        if country_code=='in':
            url = 'https://{}.search.yahoo.com/search?p='.format(country_code) + \
                urllib.parse.quote_plus(query)  # check live debug
            print("'{}' generated as the query url".format(url))
            return url
        else:
            url = 'https://{}.search.yahoo.com/search?p='.format(country_code) + \
                urllib.parse.quote_plus(query)  # check live debug
            print("'{}' generated as the query url".format(url))
            return url

    def text_result_parsing(self,page):
        """
        page: <class 'requests.models.Response'>
                returned object through requests after querying yahoo.in

        Parses the page and gets the required links
        
        Returns a list of URLs as the Yahoo search result page would have them
        """
        tree = html.fromstring(page.content)
        links = tree.xpath("//a[contains(@class, 'ac-algo fz-l ac-21th lh-24')]/@href")
        link_values=[]
        for link in links:
            link_cleaned=(urllib.parse.unquote_plus(link))
            if link_cleaned.count('www')==1:
                if "//RK=" in link_cleaned:
                    link_values.append(link_cleaned.split(':')[-1].split('//RK=')[0][2:])
                elif "/RK=" in link_cleaned:
                    link_values.append(link_cleaned.split(':')[-1].split('/RK=')[0][2:])
            else:
                if "//RK=" in link_cleaned:
                    temp_link=link_cleaned.split(':')[-1].split('//RK=')[0][2:]
                    if temp_link.startswith('www.'):
                        link_values.append(temp_link)
                    else:
                        link_values.append('www.'+temp_link)
                elif "/RK=" in link_cleaned:
                    temp_link=link_cleaned.split(':')[-1].split('//RK=')[0][2:]
                    if temp_link.startswith('www.'):
                        link_values.append(temp_link)
                    else:
                        link_values.append('www.'+temp_link)
        return link_values
    
    def search(self, query):
        """
        query:string

        Queries the search_engine for the specified query

        """
        print("""Initiating search for "{}" """.format(query))
        url = self.text_query_encoding(query)

        print("Getting the page")
        # page = self.get_page(url,proxy_pool=proxies)
        page = self.serve_engine.get_page(url)

        print("Parsing the results")
        links = self.text_result_parsing(page)

        print("""The search for "{}" results is now over.""".format(query))

        return links

class bing(search_engine):

    def __init__(self,serving_engine):
        super(bing, self).__init__(server)

    def text_query_encoding(self,query):
        """
        query : string
        Query to be made through bing search

        Encodes the URL as needed by bing for the query to be valid
        """
        url = 'https://www.bing.com/search?q=' + \
            urllib.parse.quote_plus(query)  # check live debug
        print("'{}' generated as the query url".format(url))
        return url

    def text_result_parsing(self,page,bing_help_url_inclusion=False):
        """
        page: <class 'requests.models.Response'>
                returned object through requests after querying bing.com

        Parses the page and gets the required links
        
        bing_help_url_inclusion: Boolean <TRUE/FALSE>
        
        Parameter for inclusion of URLs that direct to the Bing help page.
        This will be useful for results that are looking exactly for these
        kind of results.
        Filters out the URLs in this format : 'https://go.microsoft.com/fwlink/?' and 
        also includes a check for 'http' .
        
        Returns a list of URLs as Bing search result page would have them
        """
        tree = html.fromstring(page.content)
        bing_help_url_https='https://go.microsoft.com/fwlink/?'
        bing_help_url_http='http://go.microsoft.com/fwlink/?'
        tree = html.fromstring(page.content)
        links = tree.xpath("//a[contains(@href, 'http')]")
        link_values=[]
        for link in links:
            link_values.append(link.values())
        final_links=[]
        for link in link_values:
            for href in link:
                if bing_help_url_inclusion==False:
                    if href.startswith('http') and \
                    bing_help_url_https not in href and bing_help_url_http not in href :
                        final_links.append(href)
                else:
                    if href.startswith('http'):
                        final_links.append(href)
        return final_links  

    def search(self, query):
        """
        query:string

        Queries the search_engine for the specified query

        """
        print("""Initiating search for "{}" """.format(query))
        url = self.text_query_encoding(query)

        print("Getting the page")
        # page = self.get_page(url,proxy_pool=proxies)
        page = self.serve_engine.get_page(url)

        print("Parsing the results")
        links = self.text_result_parsing(page)

        print("""The search for "{}" results is now over.""".format(query))

        return links

google_search=google(server)
bing_search=bing(server)
yahoo_search=yahoo(server)
