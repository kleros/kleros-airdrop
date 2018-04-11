import csv

from config import config

from telethon import TelegramClient

from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetParticipantsRequest

from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import InputChannel

def get_telegram_usernames(write_results = True):
    print('Fetching telegram followers... This may take a few minutes')
    api_id = config['TELEGRAM']['ID'] # Your api_id
    api_hash = config['TELEGRAM']['HASH'] # Your api_hash
    phone_number = config['TELEGRAM']['PHONE'] # Your phone number

    client = TelegramClient(phone_number, api_id, api_hash)
    client.session.report_errors = False
    client.connect()

    # will need to enter code from message if session is not active
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))


    channel = client(ResolveUsernameRequest(config['TELEGRAM']['CHANNEL'])) # Your channel

    input_channel = InputChannel(channel.chats[0].id, channel.chats[0].access_hash)

    offset = 0
    limit = 100
    all_participants = []

    # Can pull up to 10000 participants in one shot. Will need to filter if you have more users than that.
    while True:
        participants = client(GetParticipantsRequest(input_channel, ChannelParticipantsSearch(''), offset, limit, 0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
        print(offset)

    telegram_usernames = []
    for participant in all_participants:
        if participant.username:
            telegram_usernames.append(participant.username.lower())
    # telegram_usernames = [_user.username.lower() for _user in all_participants]
    if write_results:
        telegram_file = open('telegram_usernames.csv', 'w')
        telegram_writer = csv.writer(telegram_file, quoting=csv.QUOTE_ALL)

        for username in telegram_usernames:
            telegram_writer.writerow([username])

    return telegram_usernames
