import authorize as au
import datetime
import json


class Actions:

    USER = 'me'

    def __init__(self):
        pass

    def get_params(self):
        with open("params.json", "r") as params:
            data = json.load(params)

        from_id = data["from"]
        # Before date format should be in 'YYYY/MM/DD'
        before_date = data["before-date"]
        action = data["action"]

        return [from_id, before_date, action]

    def get_messages(self, service):
        params = self.get_params()
        from_id = params[0]
        before_date = params[1]
        USER = self.USER

        try:
            datetime.datetime.strptime(before_date, '%Y/%m/%d')
        except:
            raise ValueError("Incorrect date format, should be YYYY/MM/DD")

        search_query = 'from:' + from_id + ' before:' + before_date

        response = service.users().messages().list(
            userId=USER, q=search_query).execute()
        messages = []

        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId=USER, q=search_query, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages

    def trash_messages(self, service):
        messages = self.get_messages(service)
        msg_ids = []
        USER = self.USER

        for message in messages:
            msg_id = message['id']
            msg_ids.append(msg_id)

        body = {"ids": msg_ids, "removeLabelIds": [
            "INBOX", "UNREAD"], "addLabelIds": ["TRASH"]}
        try:
            service.users().messages().batchModify(userId=USER, body=body).execute()
        except:
            print('No messages returned with this search')

    def archive_messages(self, service):
        messages = self.get_messages(service)
        msg_ids = []
        USER = self.USER

        for message in messages:
            msg_id = message['id']
            msg_ids.append(msg_id)

        body = {"ids": msg_ids, "removeLabelIds": ["INBOX", "UNREAD"]}
        try:
            service.users().messages().batchModify(userId=USER, body=body).execute()
        except:
            print('No messages returned with this search')

    def main(self):
        service = au.Authorization().authorize()
        params = self.get_params()

        if params[2] == 'trash':
            self.trash_messages(service)
        elif params[2] == 'archive':
            self.archive_messages(service)


if __name__ == '__main__':
    Actions().main()
