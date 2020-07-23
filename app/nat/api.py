import json

from app.api import get_data, post_data

nat_path = '/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/ftdnatpolicies?limit=1000&expanded=true'

all_nat_rules_path = '/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/ftdnatpolicies/{}/natrules?limit=1000&expanded=true'

auto_nat_rules_path = '/api​/fmc_config​/v1​/domain​/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy​/ftdnatpolicies​/{}​/autonatrules?limit=1000&expanded=true'
manual_nat_rules_path = '/api​/fmc_config​/v1​/domain​/e276abec-e0f2-11e3-8169-6d9ed49b625f​/policy​/ftdnatpolicies​/{}​/manualnatrules​?limit=1000&expanded=true' 

manual_nat_rules_path_post = '/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/ftdnatpolicies/{}/manualnatrules'
#manual_nat_rules_path = '/api​/fmc_config​/v1​/domain​/e276abec-e0f2-11e3-8169-6d9ed49b625f​/policy​/ftdnatpolicies​/{}​/manualnatrules​?limit=1000&expanded=true'  

acp_fmc_json_directory = 'app\\temp\\nat\\json\\fmc\\' 
nat_post_json_directory = 'app\\temp\\nat\\json\\post\\'


def get_nat(server, auth_token):
    
    elements = []

    def get_natr(nat_id, nat_name):
        nat_rules = get_data(server, all_nat_rules_path.format(nat_id), auth_token)
        
        for rule in nat_rules:
            del rule['links']
            del rule['id']
            elements.append(rule)

        json_save(nat_post_json_directory, elements, nat_name)

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