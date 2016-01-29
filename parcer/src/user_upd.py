from pymongo import MongoClient
from bs4 import BeautifulSoup
import share

client = MongoClient(share.MONGODB_SERVER)
db = client[share.MONGODB_NAME]
collection = db[share.MONGODB_COLLECTION]


def main():
    soup_userdb_cfg = BeautifulSoup(open(share.USERDB_CFG_PATH, encoding='UTF-8').read(), 'html.parser')
    soup_winroute_cfg = BeautifulSoup(open(share.WINROUTE_CFG_PATH, encoding='UTF-8').read(), 'html.parser')
    userdb_list = share.get_field_list(soup_userdb_cfg.find('list', attrs={'name': 'UsersData'}).find_all('listitem'),
                                       share.USERDB_FIELDS)
    winroute_list = share.get_field_list(soup_winroute_cfg.find('list', attrs={'name': 'AutoLogins'}).find_all('listitem'),
                                         share.WINROUTE_FIELDS)

    for user in userdb_list:
        dct = {
            'uuid': user['UUID'].lower(),
            'name': user['Name'].lower(),
            'week_up': None,
            'week_down': None,
            'month_up': None,
            'month_down': None,
            'quota_week': user['QuotaWeek'],
            'quota_month': user['QuotaMonth'],
            'ip': [],
        }

        for e in filter(lambda x: user['UUID'].lower() == x['UUID'].lower(), winroute_list):
            dct['ip'].append(e['IpAddr'])
        if not dct['ip']:
            continue

        doc = collection.find_one_and_update({'uuid': dct['uuid']}, {'$set': {
            'uuid': dct['uuid'],
            'name': dct['name'],
            'quota_week': dct['quota_week'],
            'quota_month': dct['quota_month'],
        }})

        if doc is None:
            collection.insert(dct)

    client.close()


if __name__ == '__main__':
    main()


