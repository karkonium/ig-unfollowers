import time
import requests
import pandas as pd
from datetime import datetime
from tqdm import tqdm


class IgService:
    def __init__(self):
        self.session = requests.Session()
        self.user_id = None
        self.total_following_count = None
        self.total_follower_count = None


    def _get_csrf_token(self):
        self.session.get("https://www.instagram.com/accounts/login/")
        return self.session.cookies.get("csrftoken")


    def login(self, username, password):
        # Get the CSRF token by visiting the login page
        csrf_token = self._get_csrf_token()
        if not csrf_token:
            raise Exception("Failed to get CSRF token")
        
        # Headers required for the login request
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf_token
        }
        self.session.headers.update(headers)

        current_time = int(datetime.now().timestamp())
        payload = {
            "username": username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{current_time}:{password}',
            "queryParams": {},
            "optIntoOneTap": "false"
        }

        response = self.session.post("https://www.instagram.com/accounts/login/ajax/", data=payload)
        if response.status_code != 200 or not response.json().get("authenticated"):
            raise Exception("Login failed.")

        self.user_id = response.json()['userId']
        return self.user_id


    def _update_headers(self):
        users_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'x-asbd-id': '129477',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR3QKI1WxD2BGDYqQ2LKCyryMMsIXXQHAT85AC9znp48hi_s',
        }
        self.session.headers.update(users_headers)


    def get_follower_following_count(self):
        self._update_headers()

        response = self.session.get(
            f'https://www.instagram.com/api/v1/users/{self.user_id}/info/'
        )

        self.total_following_count = response.json()['user']['following_count']
        self.total_follower_count = response.json()['user']['follower_count']
        return self.total_following_count, self.total_follower_count
    

    def _get_friends_df(self, get_followers=False, get_following=False):
        # set followers or following first
        if get_followers and get_following:
            raise Exception("Pick one followers or following")
        elif get_followers:
            total_users_count = self.total_follower_count
            user_desc = "followers"
        elif get_following:
            total_users_count = self.total_following_count
            user_desc = "following"
        else:
            raise Exception("Pick one followers or following")
        
        user_df = pd.DataFrame()

        # initial params
        params = {
            'count': '10',
        }

        with tqdm(total=total_users_count, desc=f"Fetching {user_desc}", unit=f" {user_desc}") as pbar:
            for i in range(total_users_count): # upper bound number of request by of users
                response = self.session.get(
                    f'https://www.instagram.com/api/v1/friendships/{self.user_id}/{user_desc}/',
                    params=params,
                )

                # add users to df
                current_user_df = pd.DataFrame(response.json()['users'])[['id', 'username', 'full_name', 'is_private']]
                user_df = pd.concat([user_df, current_user_df], ignore_index=True)
                user_df.drop_duplicates(inplace=True)

                # Update the progress bar
                pbar.n = len(user_df)
                pbar.set_postfix({"Number of requests": f"{i}"})
                pbar.refresh()

                # prep for next request or stop break out of loop
                if 'next_max_id' in response.json():
                    params['max_id'] = response.json()['next_max_id']
                else:
                    break

                # take a chill pill every 10 requests
                if (i + 1) % 10 == 0:
                    time.sleep(1)
        
        return user_df    
        

    def get_followers_df(self):
        return self._get_friends_df(get_followers=True)


    def get_following_df(self):
        return self._get_friends_df(get_following=True)
