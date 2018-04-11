import csv
import sys
import argparse

from config import config
from tools.twitter import get_followers_screen_names
from tools.telegram import get_telegram_usernames

"""
This script is used to cross reference airdrop signups against twitter follower
and telegram users as per the terms of the airdrop. Note this script can take a long time
due to the rate limits imposed by the twitter api. We can only fetch 9000 twitter followers every
15 minutes. If possible pass a csv of twitter followers as an arg!
--subscribers: The .csv file from the airdrop signup. Should include a column containing twitter handle, telegram username and eth address
--twitter: Twitter follower .csv. This can be passed to avoid the long painful wait on pulling followers via the api.
--telegram: Telegram followers .csv.
"""
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--subscribers', required = True, help = 'Subscribers CSV to cross reference')
    ap.add_argument('-t', '--twitter', required = False, help = 'CSV of twitter followers screen names')
    ap.add_argument('-g', '--telegram', required = False, help = 'CSV of telegram followers usernames')

    args = vars(ap.parse_args())

    twitter_usernames = []
    # check to see if a csv of twitter followers was passed
    if not args['twitter']:
        # pull screen names from twitter api. Write results to csv
        twitter_usernames = get_followers_screen_names(config['TWITTER']['HANDLE'], True)
    else:
        with open(args['twitter']) as f:
            reader = csv.reader(f)
            # can we use map on file reader?
            for row in reader:
                twitter_usernames.append(row[0])

    telegram_followers = []
    # check to see if csv of telegram followers was passed
    if (not args['telegram']):
        # pull screen names from telegram api. Write result to csv
        telegram_followers = get_telegram_usernames(True)
    else:
        with open(args['telegram']) as f:
            reader = csv.reader(f)
            for row in reader:
                telegram_followers.append(row[0])

    # Cross reference our followers vs the subscribers csv
    # NOTE There are hardcoded indicies for Kleros' specific csv
    airdrop_file = open('airdrop.csv', 'w')
    airdrop_writer = csv.writer(airdrop_file)
    with open(args['subscribers']) as f:
        reader = csv.reader(f)
        for row in reader:
            # basic sterilization of the strings
            telegram_name = row[2]
            telegram_name = telegram_name.replace('@', '').lower()
            twitter_name = row[3]
            twitter_name = twitter_name.replace('@', '').lower()

            if twitter_name in twitter_usernames:
                if telegram_name in telegram_followers:
                    eth_address = row[6]
                    airdrop_writer.writerow([eth_address, config['TOKENS_PER_ADDRESS']])

    print('Done! Generated airdrop.csv')
