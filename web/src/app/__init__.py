import re
from flask import Flask, jsonify, render_template
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient

app = Flask(__name__)

# db setting
mongodb_client = MongoClient()
db = mongodb_client['winroute_stat']
db_col = db['user']

# basic auth
users = {
    'admin': '123'
}

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


# routes

@app.route('/')
@auth.login_required
def home():
    clients = db_col.find(dict()).sort('name')
    return render_template('home.html', clients=clients)


@app.route('/user/<user_uuid>/')
@auth.login_required
def get_user(user_uuid):
    user = db_col.find_one({'uuid': user_uuid})
    return render_template('user.html', user=user)


# # api

@app.route('/api/client/<ip_addr>/')
def api_get_client(ip_addr):
    ipv4_regex = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z')
    result = dict(status='fail', data=None, resone='wrong ip address')
    if ipv4_regex.match(ip_addr) is not None:
        data = db_col.find_one({'ip': ip_addr})
        if data is not None:
            result = dict(status='success',
                          data=dict(
                                  uuid=data['uuid'],
                                  name=data['name'],
                                  week_up=int(data['week_up']),
                                  week_down=int(data['week_down']),
                                  month_up=int(data['month_up']),
                                  month_down=int(data['month_down']),
                                  quota_week=int(data['quota_week']),
                                  quota_month=int(data['quota_month']),
                                  ip=data['ip']
                          ))
    return jsonify(result)


# template filters
@app.template_filter('to_mb')
def to_mb(s):
    try:
        return '%.2f' % (int(s)/(1024*1024))
    except ValueError:
        return s
