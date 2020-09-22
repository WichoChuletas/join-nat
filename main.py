import sys, getpass, urllib3

from app.models import UserData
from app.auth.get_token import get_token
from app.nat.api import get_nat, post_nat
from app.api import search_value_nat

#Deshabilitar Warnings de Certificado
urllib3.disable_warnings()

if __name__ == "__main__":
    print('\n')
    print('Welcome!')

    try:
        continuar = True

        while(continuar):
            print('\n')
            print("1.GET NAT from FMC")
            print("2.POST NAT to FMC")
            print("3.Search in NAT Policy")
            print("4.Salir")
            print('\n')
            option = int(input("Option : "))
            
            if option == 1:
                print('\n')
                server = input("FMC IP \n ->:").strip()
                print('\n')
                print('Enter Credentials')
                print('\n')
                username = input("Username \n ->:").strip()
                password = getpass.getpass().strip()

                user_data = UserData(username, password)

                headers = get_token(server, user_data)

                if headers is None:
                    continue

                get_nat(server, headers)

            if option == 2:

                print('\n')
                server = input("FMC IP \n ->:").strip()
                print('\n')
                print('Enter Credentials')
                print('\n')
                username = input("Username \n ->:").strip()
                password = getpass.getpass().strip()

                user_data = UserData(username, password)

                headers = get_token(server, user_data)

                if headers is None:
                    continue

                post_nat(server, headers)

            elif option == 3:

                while(True):
                    ip = str(input("IP Address \n ->:").strip())
                    search_value_nat(ip)
                    #op = str(input("Otra busqueda?(y/n) \n ->:").strip())
                    #if op == 'n' or op == 'no' or op == 'No' or op == 'NO':
                    #    break

            elif option == 4:
                sys.exit()

    except KeyboardInterrupt as ms:
        print("\n ******** Adios! ********")