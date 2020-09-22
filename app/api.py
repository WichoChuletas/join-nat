import requests, json, re
import pandas as pd
from progress.bar import Bar, ChargingBar



def get_data(server, path, auth_token):
    headers = {'Content-Type': 'application/json'}
    headers['X-auth-access-token']=auth_token
    url = 'https://' + server + path
    elements = []
    items = []
    
    
    def requester(url):

        try:

            r = requests.get( 
                url, 
                headers=headers,
                verify=False
            )
            
            status_code = r.status_code
            resp = r.text
            json_resp = json.loads(resp)
            if status_code == 200:
                return json_resp
            else:
                error = json_resp["error"]
                for mens in error["messages"]:
                    print("\n"+cleanhtml(mens["description"]))

        except requests.exceptions.HTTPError as err:
                print ("Error in connection --> "+str(err)) 
    
    json_response = requester(url)
    while True:

        items = json_response["items"] #Elementos obtenidos de response
        paging = json_response["paging"] #Datos de paging de objetos
        progress = Bar('Charging '+ items[0]["type"]+ ' Objects:', max=paging["limit"])
        for item in items:
            if item['type'] == 'AccessPolicy':   
                elements.append({ 'type': item['type'] , 'name': item['name'], 'id': item['id'] })
            else:
                elements.append(item)
            progress.next()
        progress.finish()

        if "next" in paging:
            url = paging["next"][0]
            json_response = requester(url)
        else:
            print(len(elements))
            break

    return elements

def post_data(server, path, auth_token, data, section):

    url = 'https://' + server + path + '?section=' + section + '&bulk=true'.strip()
    print(url)
    headers = {'Content-Type': 'application/json'}
    headers['X-auth-access-token']=auth_token

    def requester():

        try:
  
            r = requests.post(
                url, 
                data=json.dumps(data),
                headers=headers,
                verify=False
            )
            print(r)
            status_code = r.status_code
            resp = r.text
            
            if status_code == 201 or status_code == 202:
                print('POST SUCCESSFULLY!')
            else:
                json_resp = json.loads(resp)
                error = json_resp["error"]
                print(error)

        except requests.exceptions.HTTPError as err:
                print ("Error in connection --> "+str(err))

    requester()


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def search_value_nat(ipv4):
    csvfile = pd.read_csv('app\\temp\\nat\\csv\\policies_nat_values.csv', encoding='utf-8')
    for row in csvfile.itertuples():
        if row[2] == ipv4 or row[3] == ipv4 or row[4] == ipv4 or row[5] == ipv4:
            print("originalSource:", row[2], "\n", "originalDestination:", row[3],"\n" ,"translatedSource:", row[4], "\n", "translatedDestination:", row[5], "\n")
        #elif '.'.join((str(row[2]).split('.')[:3])) == '.'.join(ipv4.split('.')[:3]) or '.'.join((str(row[3]).split('.')[:3])) == '.'.join(ipv4.split('.')[:3]) or '.'.join((str(row[4]).split('.')[:3])) == '.'.join(ipv4.split('.')[:3]) or '.'.join((str(row[5]).split('.')[:3])) == '.'.join(ipv4.split('.')[:3]):
            #print("originalSource:", row[2], "\n", "originalDestination:", row[3],"\n" ,"translatedSource:", row[4], "\n", "translatedDestination:", row[5], "\n")
        #elif '.'.join((str(row[2]).split('.')[:2])) == '.'.join(ipv4.split('.')[:2]) or '.'.join((str(row[3]).split('.')[:2])) == '.'.join(ipv4.split('.')[:2]) or '.'.join((str(row[4]).split('.')[:2])) == '.'.join(ipv4.split('.')[:2]) or '.'.join((str(row[5]).split('.')[:2])) == '.'.join(ipv4.split('.')[:2]):
            #print("originalSource:", row[2], "\n", "originalDestination:", row[3],"\n" ,"translatedSource:", row[4], "\n", "translatedDestination:", row[5], "\n")         