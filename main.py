import os, sys, re, time, threading, requests, tkinter
from colorama import Fore, init, Style
from proxy_checker import ProxyChecker
from tkinter import filedialog

init(convert=True)
root = tkinter.Tk()
root.withdraw()
lock = threading.Lock()

class UI:
    @staticmethod
    def banner():
        banner = f'''
        \t\t\t\t██╗  ██╗     ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
        \t\t\t\t╚██╗██╔╝     ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
        \t\t\t\t ╚███╔╝█████╗██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
        \t\t\t\t ██╔██╗╚════╝██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
        \t\t\t\t██╔╝ ██╗     ██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
        \t\t\t\t╚═╝  ╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝  
        \t\t\t\t\t\t\b{Fore.LIGHTBLACK_EX}NightfallGT X Plasmonix {Style.RESET_ALL}
        '''
        return banner

    @staticmethod
    def menu():
        menu = f'''
[{Fore.LIGHTBLUE_EX}1{Style.RESET_ALL}] Scraper
[{Fore.LIGHTBLUE_EX}2{Style.RESET_ALL}] Checker'''
        return menu

def write(args):
    lock.acquire()
    sys.stdout.flush()
    print(args)
    lock.release()

def animated(args):
    l = ['|', '/', '-', '\\']
    for i in l+l+l:
        sys.stdout.write(f'\r[{Fore.LIGHTBLUE_EX}{i}{Style.RESET_ALL}] {args}')
        sys.stdout.flush()
        time.sleep(0.2)

class XProxy:
    proxy_w_regex = [
        ["http://spys.me/proxy.txt","%ip%:%port% "],
        ["http://www.httptunnel.ge/ProxyListForFree.aspx"," target=\"_new\">%ip%:%port%</a>"],
        ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json", "\"ip\":\"%ip%\",\"port\":\"%port%\","],
        ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list", '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
        ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt", '%ip%:%port% (.*?){2}-.-S \\+'],
        ["https://www.us-proxy.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://free-proxy-list.net/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://www.sslproxies.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ['https://www.socks-proxy.net/', "%ip%:%port%"],
        ['https://free-proxy-list.net/uk-proxy.html', "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ['https://free-proxy-list.net/anonymous-proxy.html', "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://www.proxy-list.download/api/v0/get?l=en&t=https", '"IP": "%ip%", "PORT": "%port%",'],
        ["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt", "%ip%:%port%"],
        ["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
        ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json", '"ip": "%ip%",\n.*?"port": "%port%",'],
        ['https://www.freeproxychecker.com/result/socks4_proxies.txt', "%ip%:%port%"],
        ['https://proxy50-50.blogspot.com/', '%ip%</a></td><td>%port%</td>'], 
        ['http://free-fresh-proxy-daily.blogspot.com/feeds/posts/default', "%ip%:%port%"],
        ['http://free-fresh-proxy-daily.blogspot.com/feeds/posts/default', "%ip%:%port%"],
        ['http://www.live-socks.net/feeds/posts/default', "%ip%:%port%"],
        ['http://www.socks24.org/feeds/posts/default', "%ip%:%port%"],
        ['http://www.proxyserverlist24.top/feeds/posts/default',"%ip%:%port%" ] ,
        ['http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http',"%ip%:%port%"],
        ['http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks', "%ip%:%port%"],
        ['http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks', "%ip%:%port%"], 
        ['https://www.my-proxy.com/free-anonymous-proxy.html', '%ip%:%port%'],
        ['https://www.my-proxy.com/free-transparent-proxy.html', '%ip%:%port%'],
        ['https://www.my-proxy.com/free-socks-4-proxy.html', '%ip%:%port%'],
        ['https://www.my-proxy.com/free-socks-5-proxy.html','%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list.html','%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list-2.html','%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list-3.html','%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list-4.html', '%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list-5.html','%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list-6.html','%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list-7.html','%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list-8.html','%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list-9.html','%ip%:%port%'],
        ['https://www.my-proxy.com/free-proxy-list-10.html','%ip%:%port%'],
                    ]

    proxy_direct = [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=5000&country=all&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=5000&country=all&ssl=all&anonymity=all',         
        'https://www.proxyscan.io/download?type=http',
        'https://www.proxyscan.io/download?type=https',
        'https://www.proxyscan.io/download?type=socks4',
        'https://www.proxyscan.io/download?type=socks5',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://github.com/TheSpeedX/PROXY-List/blob/master/socks4.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
        'https://multiproxy.org/txt_all/proxy.txt',
        'http://rootjazz.com/proxies/proxies.txt',
        'http://ab57.ru/downloads/proxyold.txt',
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
        'https://proxy-spider.com/api/proxies.example.txt',
        'https://proxylist.live/nodes/socks4_1.php?page=1&showall=1',
        'https://multiproxy.org/txt_all/proxy.txt',
        'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
        'https://www.proxy-list.download/api/v1/get?type=socks4'
        'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
        'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/proxies-socks5.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/proxies-http.txt',
        'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/proxies-socks4.txt',
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
        'https://raw.githubusercontent.com/r3xzt/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
        'https://raw.githubusercontent.com/roma8ok/proxy-list/main/proxy-list-socks5.txt',
        'https://raw.githubusercontent.com/roma8ok/proxy-list/main/proxy-list-http.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt',
        'https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/http.txt',
        'https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/https.txt',
        'https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/proxy.txt',
        'https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt',
        'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks4.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks5.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anonymous/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anonymous/socks4.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anonymous/socks5.txt',
        'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
        'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt',
        'https://github.com/mmpx12/proxy-list/blob/master/http.txt',
        'https://github.com/mmpx12/proxy-list/blob/master/socks4.txt',
        "https://www.freeproxychecker.com/result/socks5_proxies.txt",
        'https://github.com/mmpx12/proxy-list/blob/master/socks5.txt',
        'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt',
        'https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt',
        'https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/https.txt',
        'https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt',
        'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt',
        'https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt',
    ]
                       
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}

    def __init__(self):
        self.proxy_output = []
        self.scrape_counter = 0
        self.checked_counter= 0
        self.alive_counter = 0

    def _update_title(self):
        while True:
            elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start))
            os.system('title X-Proxy - Elapsed: %s ^| Scraped: %s ^| Checked: %s ^| Alive: %s' % (elapsed, self.scrape_counter, self.checked_counter, self.alive_counter))
            time.sleep(0.4)

    def file_read(self, path):
        with open(path.name, 'r', encoding='UTF-8') as f:
            text = [line.strip('\n') for line in f]
            return text

    def file_write(self, name, contents):
        with open(name, 'w', encoding='UTF-8' ) as f:
            for x in contents:
                f.write(x + '\n')

    def background_task(self):
        self.start = time.time()
        threading.Thread(target = self._update_title, daemon=True).start()

    def get_proxies(self):
        return self.proxy_output

class ProxyScrape(XProxy):
    def _scrape(self, url, custom_regex):
        try:
            proxylist = requests.get(url, timeout=5, headers=self.headers).text
            custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
            custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')

            for proxy in re.findall(re.compile(custom_regex), proxylist):
                self.proxy_output.append(proxy[0] + ":" + proxy[1])
                write(f'{Fore.LIGHTBLUE_EX}[SCRAPED]{Style.RESET_ALL} {proxy[0]}:{proxy[1]}')
                self.scrape_counter += 1

        except requests.exceptions.RequestException:
            write(f'[{Fore.RED}ERROR{Style.RESET_ALL}] Requests related error occured.')

    def scrape_regex(self):
        for source in self.proxy_w_regex:
            self._scrape(source[0], source[1])

    def scrape_direct(self):
        for source in self.proxy_direct:
            try:
                page = requests.get(source, timeout=5, headers=self.headers).text
                for proxy in re.findall(re.compile('([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}):([0-9]{1,5})'), page):
                    self.proxy_output.append(proxy[0] + ':' + proxy[1])
                    write(f'{Fore.LIGHTBLUE_EX}[SCRAPED]{Style.RESET_ALL} {proxy[0]}:{proxy[1]}')

            except requests.exceptions.RequestException:
                write(f'[{Fore.RED}ERROR{Style.RESET_ALL}] Requests related error occured.')
        

class ProxyCheck(XProxy):
    def __init__(self):
        XProxy.__init__(self)
        animated('Loading...')
        self.checker = ProxyChecker()
        os.system('cls')
        
    def check(self, list_, timeout=5):
        for x in list_:
            c = self.checker.check_proxy(x)
            if c:
                write(f"{Fore.GREEN}[ALIVE]{Style.RESET_ALL} {x} | Anonymity: {c['anonymity']}  | Timeout: {str(c['timeout'])} | Country: {c['country_code']} | Protocol: {c['protocols'][0]}")
                with open('all_alive.txt', 'a', encoding='UTF-8') as f:
                    f.write(x + '\n')
                    self.alive_counter += 1

                if c['protocols'][0] == 'http':
                    with open('http_alive.txt', 'a', encoding='UTF-8') as f:
                        f.write(x + '\n')                 

                elif c['protocols'][0] == 'socks4':
                    with open('socks4_alive.txt', 'a', encoding='UTF-8') as f:
                        f.write(x + '\n')   

                elif c['protocols'][0] == 'socks5':
                    with open('socks5_alive.txt', 'a', encoding='UTF-8') as f:
                        f.write(x + '\n') 
                else:
                    pass
                self.checked_counter += 1
   
            else:
                write(f"{Fore.RED}[DEAD]{Style.RESET_ALL} {x}")
                with open('dead_proxies.txt', 'a', encoding='UTF-8') as f:
                    f.write(x + '\n')
                self.checked_counter += 1

def main():
    x = UI()
    p = ProxyScrape()
    os.system('cls & mode 140,20 && title X-Proxy ^| AIO Proxy Tool')
    print(x.banner())
    print(x.menu())
    try:
        user_input = int(input(f'[{Fore.LIGHTBLUE_EX}?{Style.RESET_ALL}] Choice> '))
        if user_input == 1:
            os.system('cls')
            print(x.banner())
            p.background_task()
            animated('Scraping proxies...')
            p.scrape_regex()
            p.scrape_direct()

            output = p.get_proxies()
            animated('Checking for duplicates..')
            print(f'[{Fore.GREEN}*{Style.RESET_ALL}] {len(output)}')
            clean_output = list(set(output))
            print(f'[{Fore.LIGHTBLUE_EX}+{Style.RESET_ALL}] Length after removing duplicates:', len(clean_output))

            animated('Writing to scraped.txt..')
            p.file_write('scraped.txt', clean_output)
            print(f'[{Fore.GREEN}+{Style.RESET_ALL}] Finished.')
            os.system('pause>nul')

        elif user_input == 2:
            pc = ProxyCheck()
            os.system('cls')
            print(x.banner())
            input(f'[{Fore.LIGHTBLUE_EX}#{Style.RESET_ALL}] Press ENTER to open proxy path')
            path = filedialog.askopenfile(parent=root, mode='rb', title='Path', filetype=(('txt', '*.txt'), ('All files', '*.txt')))
            proxy_list = pc.file_read(path)
            thread_count = int(input(f'[{Fore.LIGHTBLUE_EX}>{Style.RESET_ALL}] Enter number of threads [e.g 200]: '))
            animated('Loading..')
            threads = []
            os.system('cls')
            print(x.banner())
            pc.background_task()
            for i in range(thread_count):
                t = threading.Thread(target=pc.check, args= (proxy_list[int(len(proxy_list) / thread_count * i): int(len(proxy_list)/ thread_count* (i+1))],))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            print(f'[{Fore.GREEN}+{Style.RESET_ALL}] Finished.')
            os.system('pause>nul')
        else:
            main()
    except ValueError:
        main()

if __name__ == '__main__':
    main()
