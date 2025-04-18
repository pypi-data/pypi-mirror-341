# from datetime import date
import os
import re
import time
import requests
from tqdm import tqdm
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import json


def find_id_in_script(script_text, id_pattern):
    pattern = re.compile(id_pattern)
    matches = pattern.findall(script_text)
    return matches

class Instapy:
    def __init__(self, cookies, headers=None, turnstile=None):
        self.cookies = cookies
        self.headers = headers
        self.turnstile = turnstile
        
        if self.turnstile is None:
            raise ValueError("You need to provide the turnstile token when creating the instapy instance")

    def get_user_id(self, username=None):

        print("Getting user id for user: ", username)

        if username is None:
            raise ValueError("Username is required")
        if self.cookies is None:
            raise ValueError("You need to provide the instagram cookie when creating the instapy instance")
        

        response = requests.get(f'https://www.instagram.com/{username}/', cookies=self.cookies)

        if response.status_code == 200:
            user_id = find_id_in_script(response.text, r'"id":"(\d+)"')[0]
            print("User id for", username, "is:", user_id)
            return user_id
        else:
            print("server returned ", response.status_code, " status code")
            raise ValueError("Error getting user id")
        
    def get_new_dm_links(self, user=None, user_id=None):
        if user_id is None:
            if user is None:
                raise ValueError("User id is required for getting the reels")
            user_id = self.get_user_id(user)
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'dpr': '1',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.114", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'viewport-width': '1920',
        }

        response = requests.get(f'https://www.instagram.com/direct/t/{user_id}/', cookies=self.cookies, headers=headers)
    

        matchs = find_id_in_script(response.text, r'"payload":"(.*?)","dependencies":')
     
        if matchs: 
            payload_value = matchs[0].replace("\\u0022", "\"").replace("\\u0026", "&").replace("\\u0027", "'").replace("\\u003c", "<").replace("\\u003e", ">").replace("\\u003d", "=").replace("\\" , "")
            links  = re.findall(r'www\.instagram\.com[^\s"\']*', payload_value)
            cleaned_links = [link.replace('\\\\\\', '').replace('\\', '').split("/?id")[0] for link in links]
            formatted_links = [f'https://{link}' for link in cleaned_links]
            unique_links = list(set(formatted_links))
            return unique_links
        else:
            print("No payload found")
    
    def get_reels_links(self, user, count=12, user_id=None):
        ### This function get a user reels links from his main page

        if user is None:
            raise ValueError("User id is required for getting the reels")
        if self.cookies is None:
            raise ValueError("You need to provide the instagram cookie when creating the instapy instance")
        
        if user_id is None:
            user_id = self.get_user_id(user)

        variables = {'variables': f'{{"data":{{"count":{count},"include_relationship_info":true,"latest_besties_reel_media":true,"latest_reel_media":true}},"username":"{user}","__relay_internal__pv__PolarisIsLoggedInrelayprovider":true,"__relay_internal__pv__PolarisFeedShareMenurelayprovider":true}}'}
        
        data = {
            'av': user_id,
            'doc_id': '8388565321195220',
        }
        data.update(variables)
        print("Getting reels links")
        response = requests.post('https://www.instagram.com/graphql/query', cookies=self.cookies,  data=data)
        links = []
        if response.status_code == 200:
            nodes = response.json()['data']['xdt_api__v1__feed__user_timeline_graphql_connection']['edges']
            for node in nodes:
                video_url = node['node']['code']
                links.append(video_url)
            last_id = nodes[-1]['node']['id']
        else:
            print("server returned ", response.status_code, " status code")
            raise ValueError("Error getting reels links")
        
        for i in range(12, count, 12):
            try:
                variables = {'variables': f'{{"after":"{last_id}","before":null,"data":{{"count":{count - i},"include_relationship_info":true,"latest_besties_reel_media":true,"latest_reel_media":true}},"username":"{user}","__relay_internal__pv__PolarisIsLoggedInrelayprovider":true,"__relay_internal__pv__PolarisFeedShareMenurelayprovider":true}}'}
                data = {
                    'av': user_id,
                    'doc_id': '8388565321195220',
                }
                data.update(variables)
                response = requests.post('https://www.instagram.com/graphql/query', cookies=self.cookies,  data=data)
                if response.status_code == 200:
                    nodes = response.json()['data']['xdt_api__v1__feed__user_timeline_graphql_connection']['edges']
                    for node in nodes:
                        video_url = node['node']['code']
                        links.append(video_url)
                else:
                    print("server returned ", response.status_code, " status code")
                    raise ValueError("Error getting reels links")
                if len(nodes) == 0:
                    break
                last_id = nodes[-1]['node']['id']
            except:
                print("error getting all the reels")

        urls = [f'https://www.instagram.com/reel/{url}/' for url in links]
        if count != len(urls) and count < len(urls):   
            urls = urls[0:count]
        print("Got:", len(urls), "reels links")
        return urls
    
    def get_job_id(self, link):
        ### Initializes the download job for a reel

        if link is None:
            raise ValueError("Error getting job id for reel download. (This is an internal error)")
        
        print("Getting job id...")

        headers = {
            'accept':
            '*/*',
            'accept-language':
            'en-US,en;q=0.9',
            'content-type':
            'application/json;',
            'origin':
            'https://publer.io',
            'priority':
            'u=1, i',
            'referer':
            'https://publer.io/',
            'sec-ch-ua':
            '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile':
            '?0',
            'sec-ch-ua-platform':
            '"Windows"',
            'sec-fetch-dest':
            'empty',
            'sec-fetch-mode':
            'cors',
            'sec-fetch-site':
            'same-site',
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        json_data = {
            "url": link,
            "token": self.turnstile,
            "macOS": False
        }

        response = requests.post('https://app.publer.com/tools/media', headers=headers, json=json_data)
        
        if response.status_code == 200:  
            job_id = response.json()["job_id"]
            print("Job id for the download is:", job_id)
            return job_id
        else:
            raise ValueError("Error getting job id for download")
    
    def download_reels(self, reels_links=None, count=12, user=None, user_id=None, path="videos"):
        if reels_links is None:
            if user is None:
                raise ValueError("You need to provide user")
            if user_id is None:
                user_id = self.get_user_id(user)
            
            reels_links = self.get_reels_links(user, count, user_id)

        print("Starting the download process...")
        for link in reels_links:
            job_id = self.get_job_id(link)

            # INIT JOB
            response = requests.get(f'https://app.publer.io/api/v1/job_status/{job_id}')
            print("Waiting for download to start")
            time.sleep(1)

            # WAIT FOR VIDEO TO BE READY FOR DOWNLOAD
            while response.json()["status"] != "complete":
                response = requests.get(f'https://app.publer.io/api/v1/job_status/{job_id}')
                time.sleep(1)

            downloadLink = response.json()['payload'][0]['path']
            title = f"{link.split('/')[-2] if link.split('/')[-1] == '' else link.split('/')[-1]}.mp4"
            os.makedirs(path, exist_ok=True)


            print("Downloading reel...")
            response = requests.get(downloadLink, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            with open(f"{path}/{title}", 'wb') as f:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
            progress_bar.close()
            print("Download video", reels_links.index(link) + 1, "of", len(reels_links))
    def scrape_page(self, user, count=12, path="videos"):
        user_id = self.get_user_id(user)
        reels_links = self.get_reels_links(user, count=count, user_id=user_id)
        self.download_reels(reels_links=reels_links, path=path)

    def set_turnstile(self, turnstile):
        self.turnstile = turnstile



# SCOPE = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]
# HEADERS = ["user", "link", "sender", "receiver", "download date"]

# class Sheet:
#     def __init__(self, creds_path=None, scope=SCOPE, headers=HEADERS):
#         if creds_path is None:
#             raise ValueError("You need to provide the path to the credentials file")
#         self.credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
#         with open(creds_path) as f:
#             self.creds_data = json.load(f)
#         self.client = gspread.authorize(self.credentials)
#         self.sheet = self.client.open("djaltireddit instagram download").sheet1

#         existing_headers = self.sheet.row_values(1)  # Get the first row values

#         if existing_headers != headers:
#             # workself.sheet.delete_row(1)  # Uncomment if you want to clear it
#             self.sheet.insert_row(headers, 1) 

#     def check_links(self, links):
#         sheet_links = self.sheet.col_values(2)
#         return [link for link in links if link not in sheet_links]

#     def add_link(self, link, user, sender, receiver, download_date):
#         self.sheet.append_row([user, link, sender, receiver, download_date])
    
#     def download_new_dms(self, instapy=None, user=None, user_id=None):
#         if instapy is None:
#             raise ValueError("You need to provide the instapy instance")
#         print("Getting DMs links")
#         links = instapy.get_new_dm_links(user, user_id)
#         print("Got from DMs:", len(links))
#         new_links = self.check_links(links)
#         print("New links found:", len(new_links))
#         for link in new_links:
#             instapy.download_reels([link])
#             self.add_link(link, "djaltireddit", "djaltireddit", "motivault", date.today().strftime("%Y-%m-%d"))
#             print("Downloaded: ", link)


    
    

   