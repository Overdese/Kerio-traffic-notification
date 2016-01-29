
USERDB_CFG_PATH = "UserDB.cfg"
WINROUTE_CFG_PATH = "winroute.cfg"
STATS_CFG_PATH = "stats.cfg"

MONGODB_SERVER = "localhost"
MONGODB_NAME = "winroute_stat"
MONGODB_COLLECTION = "user"


USERDB_FIELDS = [
    'UUID',
    'Name',
    # 'AccStatus',
    # 'WWWFilter',
    # 'UseTemplate',
    # 'Rights',
    # 'AdmFilter',
    # 'QuotaDayEnabled',
    # 'QuotaDayType',
    # 'QuotaDay',
    # 'QuotaWeekEnabled',
    # 'QuotaWeekType',
    'QuotaWeek',
    # 'QuotaMonthEnabled',
    # 'QuotaMonthType',
    'QuotaMonth',
    # 'QuotaAction',
    # 'QuotaSendAlert',
    # 'Lang',
    # 'DontUseLangTemp',
    # 'DetectedLang',
    # 'PhotoTimestamp'
    ]

WINROUTE_FIELDS = [
    # 'Username',
    'UUID',
    'IpAddr',
    # 'IpGroup',
    # 'IpType',
    ]

STAT_FIELDS = [
    'Id',
    # 'Name',
    # 'DayUp',
    # 'DayDown',
    'WeekUp',
    'WeekDown',
    'MonthUp',
    'MonthDown',
    # 'TotalUp',
    # 'Since',
    # 'Timestamp',
    # 'FullName'
    ]


def get_field_list(soup_obj, fields):
    lst = list()
    for e in soup_obj:
        dct = dict()
        for field in fields:
            try:
                dct[field] = e.find(attrs={'name': field}).text
            except AttributeError:
                dct[field] = None
        lst.append(dct)
    return lst
