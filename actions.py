import authorize as au
import pandas as pd
import datetime

from_id = 'order@zomato.com'
# Before date format should be in 'YYYY/MM/DD'
before_date = '2019/01/01'
user_id = 'me'


def get_messages(service):
    try:
        datetime.datetime.strptime(before_date, '%Y/%m/%d')
    except:
        raise ValueError("Incorrect date format, should be YYYY/MM/DD")

    search_query = 'from:' + from_id + ' before:' + before_date

    response = service.users().messages().list(userId=user_id, q=search_query).execute()
    messages = []

    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId=user_id, q=search_query, pageToken=page_token).execute()
        messages.extend(response['messages'])

    return messages


def main():
    service = au.Authorization().authorize()
    messages = get_messages(service)

    df = pd.DataFrame(messages)
    df.to_csv('Message_List.csv')


if __name__ == '__main__':
    main()