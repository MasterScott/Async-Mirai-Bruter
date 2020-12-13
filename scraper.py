import aiohttp, asyncio, socket
from colorama import *


class Scraper:
    def __init__(self):
        self.url = "https://urlhaus-api.abuse.ch/v1/tag/"
        self.data = {"tag":"mirai"} # Change the tag if you would like. Not suggested.

    def remove_duplicates(self, urls):
        return list(dict.fromkeys(urls))

    async def get_urls(self):
        print(Fore.GREEN+"[+] Scraping Url Haus For Skids Malware [+]")
        urls = []
        async with aiohttp.ClientSession() as s:
            req = await s.post(self.url, data=self.data)
            res = await req.json()
            for url in res["urls"]:
                malwareUrl = url["url"]
                splitUrl = malwareUrl.split("/")
                urls.append(str(splitUrl[2]))
            print(Fore.YELLOW+f"[+] Damn Found {len(urls)} Pieces Of Skids Malware [+]")

            nonDupes = self.remove_duplicates(list(urls))
            cleanList = self.clean_list(nonDupes)

            return cleanList # This is all we want from this function

    def clean_list(self, urls):
        ips = []
        for ip in urls:
            try:
                f = ip.split(":")
                ip = f[0]
                resDomain = socket.gethostbyname(ip)
                ips.append(resDomain)
            except:
                pass # DAMN BARE EXCEPTION IDGAF!
        return self.remove_duplicates(ips)
