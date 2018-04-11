import tweepy
import csv

from config import config

CONSUMER_KEY = config['TWITTER']['KEY']
CONSUMER_SECRET = config['TWITTER']['SECRET']
ACCESS_TOKEN = config['TWITTER']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = config['TWITTER']['ACCESS_TOKEN_SECRET']

# Oauth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True, retry_count = 3, retry_delay = 60)

# Function to get followers for an account. Uses Cursor to handle rate limiting
def get_followers_screen_names(root_screen_name, write_results=True):
    print('Fetching twitter followers... This may take a few minutes')
    followers_ids = []

    # Fetch all follower id's.
    # NOTE: Pulling followers directly is rate limited to 1500/15 minutes
    for page in tweepy.Cursor(api.followers_ids, id = root_screen_name).pages():
        followers_ids.extend(page)

    # Fetch user data in batches of 100. Rate limited to 9000/15 minutes
    followers = []
    search_place = 0
    run = True
    while run:
        if (100 * search_place) > (len(followers_ids)):
            run = False
            break
        followers.extend(
            api.lookup_users(
                user_ids=followers_ids[search_place*100:(search_place + 1)*100]
                )
            )
        search_place += 1
        print(search_place * 100)

    screen_names = [user.screen_name.lower() for user in followers]
    if write_results:
        # write a new csv with twitter followers
        twitter_csv = open('twitter_followers.csv', 'w')
        twitter_writer = csv.writer(twitter_csv, quoting=csv.QUOTE_ALL)
        for screen_name in screen_names:
            twitter_writer.writerow([screen_name])

    return screen_names
