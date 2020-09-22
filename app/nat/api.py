import json
import pandas as pd
from app.api import get_data, post_data

nat_path = '/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/ftdnatpolicies?limit=1000&expanded=true'

all_nat_rules_path = '/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/ftdnatpolicies/{}/natrules?limit=1000&expanded=true'

auto_nat_rules_path = '/api​/fmc_config​/v1​/domain​/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy​/ftdnatpolicies​/{}​/autonatrules?limit=1000&expanded=true'
manual_nat_rules_path = '/api​/fmc_config​/v1​/domain​/b9ec7a85-8030-0f91-2518-000000000000​/policy​/ftdnatpolicies​/{}​/manualnatrules​?limit=1000&expanded=true' 

manual_nat_rules_path_post = '/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/ftdnatpolicies/{}/manualnatrules'
#manual_nat_rules_path = '/api​/fmc_config​/v1​/domain​/b9ec7a85-8030-0f91-2518-000000000000​/policy​/ftdnatpolicies​/{}​/manualnatrules​?limit=1000&expanded=true'  

network_objects_path = '/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/networkaddresses?limit=1000&expanded=true'

acp_fmc_json_directory = 'app\\temp\\nat\\json\\fmc\\' 
nat_post_json_directory = 'app\\temp\\nat\\json\\post\\'


def get_nat(server, auth_token):
    
    elements = []
    items = []

    def get_natr(nat_id, nat_name):

        nat_rules = get_data(server, all_nat_rules_path.format(nat_id), auth_token)
        

        for rule in nat_rules:
            del rule['links']
            del rule['id']
            elements.append(rule)
        
        json_save(nat_post_json_directory, elements, nat_name)

        network_objects = get_data(server, network_objects_path, auth_token)
        
        for rule in network_objects:
            del rule['links']
            del rule['id']
            del rule['metadata']
            items.append(rule)

        json_save(acp_fmc_json_directory, items, "networks")

        generate_csv(elements)
        search_value_objects()


    continuar = True

    while(continuar):
        nats = get_data(server, nat_path, auth_token)
        
        print('\n')
        
        i = 0
        for i in range(0, len(nats)):
            print( str(i) + '. ' + nats[i]['name'])
            try:
                print('--> Description: '  + nats[i]['description'])
            except:
                print('--> Description: N/A')

        print(str(i+1) + '. ' + 'Salir')

        print('\n')
        
        option = int(input("Option : "))
    
        if option == len(nats):
            continuar = False

        else :
            option_nat = nats[option]
            #print(option_acp['id'])

            get_natr(option_nat['id'], option_nat['name'])
            elements = []

def post_nat(server, auth_token):
    elements = []
    sections = []
    typesnat = []
    before_auto = []
    after_auto = []
    continuar = True

    while(continuar):

        acps = get_data(server, nat_path, auth_token)

        print('\n')
        i = 0
        for i in range(0, len(acps)):
            print( str(i) + '. ' + acps[i]['name'])
            try:
                print('--> Description: '  + acps[i]['description'])
            except:
                print('--> Description: N/A')
        print(str(i+1) + '. ' + 'Salir')

        print('\n')
        option = int(input("Option : "))
    
        if option == len(acps):
            continuar = False

        else :
            option_acp = acps[option]
            print(option_acp['id'])
            print('\n')
            directory = input("JSON file : ")

            data = json_open(directory)

            before_auto, after_auto = split_nat_rules(data)

            post_data(server, manual_nat_rules_path_post.format(option_acp['id']), auth_token, before_auto, 'before_auto')
            post_data(server, manual_nat_rules_path_post.format(option_acp['id']), auth_token, after_auto, 'after_auto')


def json_save(directory, json_acr, acp_name):
    with open('{}{}.json'.format(directory, acp_name), 'w+') as json_file:
        json.dump(list(json_acr), json_file, indent=4)

def json_open(directory):
    with open(directory) as json_file:
        return json.load(json_file)

def name_rules(name, sufix):
    name = name + '-' + sufix
    if len(name) > 30:
        name = name[:30]
        return name
    return name

def namer_rules(rules, sufix):
    new_rules = []
    for rule in rules:
        rule['name'] = name_rules(rule['name'], sufix)
        new_rules.append(rule)
    return new_rules

def split_nat_rules(rules):
    before_auto = []
    after_auto = []
    for rule in rules:
        if rule['metadata']['section'] == 'BEFORE_AUTO':
            del rule['metadata']
            before_auto.append(rule)
        elif rule['metadata']['section'] == 'AFTER_AUTO':
            del rule['metadata']
            after_auto.append(rule)
    return before_auto, after_auto

def duplicates(duplicates, name):
    singles = []
    for duplicate in duplicates:
        if duplicate not in singles:
            singles.append(duplicate)
    
    print('\n'+name)
    for single in singles:
        print(single)
    return singles

def generate_csv(nat_policy):
    csv_nat_policy = []
    for rule in nat_policy:
        row = {
            'originalSource': rule['originalSource']['name'] if 'originalSource' in rule else 'Any',
            'originalDestination': rule['originalDestination']['name'] if 'originalDestination' in rule else 'Any',
            'translatedSource': rule['translatedSource']['name'] if 'translatedSource' in rule else 'Any',
            'translatedDestination': rule['translatedDestination']['name'] if 'translatedDestination' in rule else 'Any'  
        }
        csv_nat_policy.append(row)
    nat_policy_dataframe = pd.DataFrame(csv_nat_policy)
    nat_policy_dataframe.to_csv('app\\temp\\nat\\csv\\policies.csv')

def get_value(name):
    with open('app\\temp\\nat\\json\\fmc\\networks.json', "r+") as json_file:
        networks = json.load(json_file)
        
        for network in networks:
            
            if(network["name"].lower() == name.lower()):
                return network["value"]

def search_value_objects():
    csvfile = pd.read_csv('app\\temp\\nat\\csv\\policies.csv', encoding='utf-8')
    nat_policy = []
    for row in csvfile.itertuples():    
        rule = {
            'originalSource': get_val ue(row[2]) if row[2]!='Any' else 'Any',
            'originalDestination': get_value(row[3]) if row[3]!='Any'  else 'Any',
            'translatedSource': get_value(row[4]) if row[4]!='Any' else 'Any',
            'translatedDestination': get_value(row[5])if row[5]!='Any' else 'Any' 
        }
        print(rule)
        nat_policy.append(rule)
    nat_policy_dataframe = pd.DataFrame(nat_policy)
    nat_policy_dataframe.to_csv('app\\temp\\nat\\csv\\policies_nat_values.csv')