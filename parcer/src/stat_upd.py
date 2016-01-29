from pymongo import MongoClient
from bs4 import BeautifulSoup
import share


client = MongoClient(share.MONGODB_SERVER)
db = client[share.MONGODB_NAME]
collection = db[share.MONGODB_COLLECTION]


def main():
    soup_stat_cfg = BeautifulSoup(open(share.STATS_CFG_PATH, encoding='UTF-8').read(), 'html.parser')
    stat_list = share.get_field_list(soup_stat_cfg.find_all('listitem'), share.STAT_FIELDS)

    for stat in stat_list:
        collection.find_one_and_update({'uuid': stat['Id'].lower()},
                                       {'$set': {
                                           'week_up': stat['WeekUp'],
                                           'week_down': stat['WeekDown'],
                                           'month_up': stat['MonthUp'],
                                           'month_down': stat['MonthDown'],
                                       }})
    client.close()


if __name__ == '__main__':
    main()
