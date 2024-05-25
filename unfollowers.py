import pandas as pd
import numpy as np
import getpass

from ig_service import IgService

if __name__ == '__main__':
    username = input("Enter your ig user: ")
    password = getpass.getpass("Enter your password: ")

    ig = IgService()
    user_id = ig.login(username, password)
    print(f"Login successful; user_id: {user_id}")

    total_following_count, total_follower_count = ig.get_follower_following_count()
    print(f'Following: {total_following_count}; Followers: {total_follower_count}')

    followers_df = ig.get_followers_df()
    following_df = ig.get_following_df()

    non_followers_usernames = list(np.setdiff1d(following_df['username'], followers_df['username']))
    non_followers_usernames

    unfollowers_df = following_df[following_df['username'].isin(non_followers_usernames)].copy()
    unfollowers_df['link'] = 'https://www.instagram.com/' + following_df['username']
    print('List of unfollowers:')
    print(unfollowers_df)