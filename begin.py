#!/usr/bin/env python3
from crypt import methods
import requests
import itertools
import operator
from flask import Flask, render_template


from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    firmware = db.Column(db.String(20), nullable=False)

    def __init__(self, url, name, firmware):
        self.url = url
        self.name = name
        self.firmware = firmware

    def __repr__(self) -> str:
        return "ID: %s, %s, %s, %s" % (self.id, self.url, self.name, self.firmware) 


# def add_data(url, name, firmware):  
#   try:
#       db.session.add(Device(url, name, firmware))
#       db.session.commit()
#   except:
#     print("Add Device failed")

# def delete_data():
#     try:
#         db.session.delete()
#         db.session.commit()
#     except:
#         print("Delete Device failed")


# def clear_data():
#     meta = db.metadata
#     for table in reversed(meta.sorted_tables):
#         print("deleting")
#         db.session.execute(table.delete())
#         db.session.commit()
#     print("done")


# clear_data()
# def initializeDB(incoming_data):
#     for x in incoming_data:
#         add_data(x[0], x[1], x[2])

# Prints the devices in the server
# all_devices_api = requests.get("https://api.ipsw.me/v4/devices").json()
# print(json.dumps(j, sort_keys=True, indent=4))


device_types = ["iOS", "iPadOS", "MacOS / WatchOS"]
# all_devices = [[x['name'], x['identifier'], all_devices_api.index(x)]
#                for x in all_devices_api if "iBridge" not in x['name'] and "Developer Transition Kit" not in x["name"]]


# def filterFunction(device_list):
#     wordsToClean = ["(GSM)", "(Global)", "(WiFi)", "(Cellular)"]
#     key_func = lambda x: x[1]
#     group = itertools.groupby(sorted(device_list, key=key_func), key=key_func)
#     to_clean = [[key, [[x[0][0], x[2], x[3]] for x in list(group)]] for key,group in group]
#     cleaned  =  sorted([[x[0], '/'.join(sorted(set(' '.join(x for x in y[0].split(' ') if x not in wordsToClean) for y in x[1]))), x[1][0][1], x[1][0][2]] for x in to_clean], key=operator.itemgetter(3))
#     # initializeDB(cleaned)
#     return cleaned

# # Name, ID, URL, FW Version
# all_iPhones = [[x, requests.get(
#     "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
#     "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version'], x[2]]
#     for x in all_devices if "iPhone" in x[0]]
# grouped_iPhones = filterFunction(all_iPhones)

    

# all_iPads = [[x, requests.get(
#     "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
#     "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version'], x[2]]
#     for x in all_devices if "iPad" in x[0]]
# grouped_iPads = filterFunction(all_iPads)

# all_macs = [[x, requests.get(
#     "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
#     "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version'], x[2]] for x in all_devices if "Mac" in x[0]]
# grouped_Macs = filterFunction(all_macs)

# all_ipods = [[x, requests.get(
#     "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
#     "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version'], x[2]] for x in all_devices if "iPod" in x[0]]
# grouped_iPods = filterFunction(all_ipods)

# all_watches = [[x, requests.get("https://api.ipsw.me/v4/device/{}?type=ota".format(x[1])).json()['firmwares'][0]['url'], requests.get(
#     "https://api.ipsw.me/v4/device/{}?type=ota".format(x[1])).json()['firmwares'][0]['version'], x[2]] for x in all_devices if "Watch" in x[0]]
# grouped_Watches = filterFunction(all_watches)



grouped_iPhones = Device.query.filter(Device.name.contains('iPhone')).all()
grouped_iPads = Device.query.filter(Device.name.contains('iPad')).all()
grouped_Macs = Device.query.filter(Device.name.contains('Mac')).all()
grouped_iPods = Device.query.filter(Device.name.contains('iPod')).all()
grouped_Watches = Device.query.filter(Device.name.contains('Watch')).all()
latest_firmwares = {
    "iOS": grouped_iPhones[-1].firmware,
    "iPadOS": grouped_iPads[-1].firmware,
    "MacOS": grouped_Macs[-1].firmware,
    "WatchOS":grouped_Watches[-1].firmware,
}




@ app.route("/")
@ app.route("/home")
def home():
    return render_template('home.html', data=[device_types, grouped_iPhones, grouped_iPads, grouped_Macs, grouped_iPods, grouped_Watches, latest_firmwares])

@ app.route("/presets")
def presets():
    return render_template('presets.html')


@ app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
