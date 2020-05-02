import authorize as au
import datetime
import json

with open("params.json", "r") as params:
    data = json.load(params)

from_id = data["from"]
# Before date format should be in 'YYYY/MM/DD'
before_date = data["before-date"]
user_id = 'me'
action = data["action"]


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


def trash_messages(service):
    messages = get_messages(service)
    msg_ids = []

    for message in messages:
        msg_id = message['id']
        msg_ids.append(msg_id)

    body = {"ids": msg_ids, "removeLabelIds": ["INBOX", "UNREAD"], "addLabelIds": ["TRASH"]}
    try:
        service.users().messages().batchModify(userId=user_id, body=body).execute()
    except:
        print('No messages returned with this search')


def main():
    service = au.Authorization().authorize()

    if action == 'trash':
        trash_messages(service)


if __name__ == '__main__':
    main()
