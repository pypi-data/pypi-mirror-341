import requests
import base64
import re
import requests
import threading


class ProxiesGrabber:
    def __init__(self):
        self.list = []
        self.Checked = []
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.sites = [
            self.site1,
            self.site2,
            self.site3,
            self.site4,
            self.site5,
            self.site6,
            self.site7
        ]
        self.fetch_proxies()

    def fetch_proxies(self):
        threads = []
        for site in self.sites:
            thread = threading.Thread(target=site)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

            return False

    def site1(self):
        try:
            response = self.session.get("https://free-proxy-list.net/", headers=self.headers, timeout=5)  # noQa
            data = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b', response.text)  # noQa
            for ip in data:
                self.list.append(ip)
        except requests.RequestException:
            pass

    def site2(self):
        try:
            for page in range(1, 5):
                response = self.session.get(f"http://free-proxy.cz/en/proxylist/main/{page}", headers=self.headers)  # noQa
                data = re.findall(r'Base64.decode\("(.+?)"\).+?>(\d+)<', response.text)  # noQa
                for ip in data:
                    port = ip[1]
                    ip = base64.b64decode(ip[0]).decode('utf-8')
                    self.list.append(f"{ip}:{port}")
        except requests.RequestException:
            pass

    def site3(self):
        def requset(url):
            list = []
            try:
                response = self.session.get(url, headers=self.headers)  # noQa
                data = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b', response.text)  # noQa
                data = re.findall(r"Proxy\('(.+?)'\)", response.text)  # noQa
                for ip in data:
                    ip = base64.b64decode(ip).decode("utf-8")
                    list.append(ip)
                return list
            except requests.RequestException:
                pass

        for page in range(1, 11):
            ips = requset(f"https://proxy-list.org/english/index.php?p={page}")
            for ip in ips:
                self.list.append(ip)

    def site4(self):
        try:
            response = self.session.get("https://www.sslproxies.org/", headers=self.headers)  # noQa
            ips = re.findall(r"(\d+\.\d+\.\d+\.\d+):(\d+)", response.text)  # noQa
            for ip in ips:
                ip = f"{ip[0]}:{ip[1]}"
                self.list.append(ip)
        except requests.RequestException:
            pass

    def site5(self):
        try:
            response = self.session.get("https://hide.mn/en/proxy-list/", headers=self.headers)  # noQa
            data = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{1,8})", response.text)  # noQa
            for ip in data:
                self.list.append(f"{ip[0]}:{ip[1]}")
        except requests.RequestException:
            pass

    def site6(self):
        try:
            response = self.session.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=json", timeout=5)  # noQa
            if response.status_code == 200:
                data = [(proxy['ip'], proxy['port'])for proxy in response.json().get('proxies', [])]  # noQa
                for proxy in data:
                    ip = f"{proxy[0]}:{proxy[1]}"
                    self.list.append(ip)
        except requests.RequestException:
            pass

    def site7(self):
        try:
            url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
            response = requests.get(url)
            data = response.json()
            for ip in data['data']:
                ip = f"{ip['ip']}:{ip['port']}"
                self.list.append(ip)
        except:
            pass
