import pandas as pd
import requests
import datetime

token_auth = '23ce4867-09d8-4f7e-8d02-c93bf1eba0a6'

#df = pd.DataFrame()

def page_gares(numero_page) :
    return requests.get('https://api.sncf.com/v1/coverage/sncf/stop_areas?start_page={}'.format(numero_page), auth=(token_auth, ''))

page_initiale = page_gares(0)
item_per_page = page_initiale.json()['pagination']['items_per_page']
total_items = page_initiale.json()['pagination']['total_result']
names = []


for page in range(int(total_items/item_per_page)+1) :
    #print("je suis a la page",page)
    stations_page = page_gares(page)
    ensemble_stations = stations_page.json()
    if 'stop_areas' not in ensemble_stations:
        continue
    for station in ensemble_stations['stop_areas'] :
        #station['lat'] = station['coord']['lat']
        #station["lon"]  = station['coord']['lon']
        if 'administrative_regions' in station.keys() :
            for var_api, var_df in zip(['insee','name','label','id','zip_code'], ['insee','region','label_region','id_region','zip_code']) :
                station[var_df] = station['administrative_regions'][0][var_api]
        [station.pop(k,None) for k in ['coord','links','administrative_regions']]
        #names.append(station["name"])
        if "Biblioth" in station["name"]:
            print station
#print df
names.sort()
print names
'''
def get_next_train(train_station):
    # http://api.transilien.com/gare/87393009/depart/
    #print 'http://api.transilien.com/gare/{}/depart/'.format(train_station)
    #return requests.get('http://api.transilien.com/gare/{}/depart/'.format(train_station), auth=(token_auth, ''))
    #https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:OCE:SA:87391003/departures?datetime=20170408T170555
    myDate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return requests.get('https://api.sncf.com/v1/coverage/sncf/stop_areas/{}/departures?datetime={}'.format(train_station, myDate), auth=(token_auth, ''))

jsNextTrains = get_next_train('stop_area:OCE:SA:87545228').json()

for train in jsNextTrains:
    print train
'''
