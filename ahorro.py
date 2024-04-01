# Sistema simple "bancario" que permite las siguientes funcionalidades
# La información no era persistente porque así era el requerimiento del test.
# Se almacena en un diccionario
# Se modifica para hacer la información persistente.
# Almacena los usuarios, pass (no tiene algoritmo de seguridad), status y balance
# en un archivo .csv y guarda backup cada vez que se sale del sistema y almacena la nueva información en 
# el archivo datos.csv

# Login         : Realiza control con clave
#                 Si el usuario no existe permite darlo de alta. 
#                 Verifica la clave por comparación
#                 Inicia el usuario con un saldo de 2000
#                 Administra múltiples usuarios
#                 Bloquea al usuario después de tres intentos fallidos de la clave
    
# Depósitos     : Permite hacer depósitos
# Retiros       : Permite realizar retiros. Valida que no se pueda retirar más que el saldo actual
# Consulta      : Permite consultar el saldo de la cuenta del usuario
# Tranferencias : Permite realizar transferencias entre cuentas a diferentes usuarios
# Logout        : Permite cerrar la sesión del usuario
# Quit          : Finaliza el programa, actualiza la información el .csv y backapea el último archivo

import os
import csv
from datetime import datetime

def mensaje(mensaje) -> None:
    """ Muestra mensaje por pantalla con una pausa
    
    Keyword arguments: Mensaje a mostrar
    argument -str- string del mensaje
    Return: None
    """
    print(mensaje)
    input()

def grabaDatos(archivo)->bool:
    """Graba los datos de los usuarios en un archivo csv.
    Si el archivo existe le cambia el nombre con la hora y la fecha para back up
    y escribe el archivo con los datos nuevos con nombre pasado por parámetro
    
    Keyword arguments:
    archivo -- nombre del archivo a grabar
    Return: Devuelve True si el proceso salio bien
    Si hubo algún fallo saca un mensaje por pantalla y vuelve a dejar el último archivo grabado correctamente
    """
    if os.path.exists(archivo):
        try:
            nuevoNombre = datetime.now().strftime('%Y%m%d%H%M%S')
            os.rename(archivo, nuevoNombre + '.csv')
            
        except:
            mensaje('No se pudo renombrar el archivo. Avise a sistemas')
        
    with open(archivo, 'w', newline='') as archivo:
        campos = ['usuario', 'pass', 'status', 'balance']
        escritor_csv = csv.DictWriter(archivo, fieldnames=campos)

        escritor_csv.writeheader()  # Escribe los encabezados

        for usuario, datos in loginDatos.items():
            escritor_csv.writerow({'usuario': usuario, **datos})

    

def cargaDatos(archivo) ->bool:
    """Lee los datos de los usuarios de un archivo csv y los almacena en un diccionario loginDatos
    
    Keyword arguments:
    archivo -- nombre del archivo a leer
    Return: Devuelve un diccionario vacío si no existe el archivo o
    si hubo algún problema en la lectura del archivo. En ese caso, avisa por pantalla
    
    """
    
    if os.path.exists(archivo):
        with open(archivo, 'r') as archivo:
            try :
                lector_csv = csv.DictReader(archivo)
                diccionario = {}
                for fila in lector_csv:
                    usuario = fila['usuario']
                    datos_usuario = {
                        'pass': fila['pass'],
                        'status': fila['status'],
                        'balance': int(fila['balance'])
                    }
                    diccionario[usuario] = datos_usuario
                return diccionario
            except:
                mensaje('Hubo inconvenientes en la lectura de los datos. La información puede no estar actualizada')
                return {}
    else:
        return {}
    
def createUser(usuario)-> None:
    """Crea un nuevo usuario, valida la clave por coincidencia
    e incia con un saldo de 2000
    
    Keyword arguments:
    usuario (str) : Nombre de usuario
    Return: None
    
    """
    while True:
        os.system('clear')
        print(f"Usuario : {usuario}")
        clave = input( 'Ingrese su clave   :')
        claveControl = input('Reingrese su clave :')
        if clave != claveControl:
            mensaje("Las claves no coinciden. Reintente")
        else:
            loginDatos[usuario.lower()] = {
                        'pass':clave,
                        'status':'ok',
                        'balance':2000}

            mensaje("Usuario dado de alta.")
            return
    
def login() ->bool:
    """Controla el acceso al sistema
        Validando usuario y password
        Máximo tres intentos, si falla no deja hacer transacciones
    
    Keyword arguments: None

    Return: True si valida usuario y contraseña
            False si no valida
            """
    
    while True:
        os.system('clear')
        usuario  = input('Ingrese el usuario :')
        if usuario == '':
            break
        if usuario.lower() in loginDatos :
            if loginDatos[usuario]['status'] == 'block':
                mensaje('Usuario bloqueado. Comuníquese con el banco.')
                exit()
            for i in range(3):
                os.system('clear')
                print('Ingrese el usuario :' + usuario)
    
                clave = input('Ingrese la clave   :')
                if clave == loginDatos[usuario]['pass']:
                    currentUser['user'] = usuario.lower()
                    return True

                else:
                    mensaje(f'Clave incorrecta. Quedan {2 - i } intentos. Presione una tecla para reintentar')

            loginDatos[usuario]['status'] = 'block'
            mensaje(f'Usuario bloqueado. Presione una tecla para seguir')

            break
        else:
            if input('Usuario inexistente. Desea darlo de alta (s/n)? ').lower() == 's':
                createUser(usuario)
                return False
            
    return False

def deposits() ->None:
    """Incrementa el valor del balance según lo ingresado
    Valida que se ingrese un entero
    Sale de la funcion si no se ingresa nada
    
    Return : None
    """
    
    while True:
        os.system('clear')
        print('Depósitos')
        print('---------')
        monto = input('Ingrese el monto a depositar : ')
        if monto == '':
            break
        try:
            monto = int(monto)
            loginDatos[currentUser['user']]['balance'] += monto
            mensaje(f"El monto fue acreditado a su cuenta. Saldo total {loginDatos[currentUser['user']]['balance']}")
            break
        except:
            mensaje('El monto debe ser un importe entero. Reintente')
        
def widthdraws() ->None:
    """Disminuye el valor del balance según lo ingresado
    Valida que se ingrese un entero
    Sale de la funcion si no se ingresa nada
    
    Return : None
    """
    while True:
        os.system('clear')
        print('Retiros')
        print('-------')
        monto = input('Ingrese el monto a retirar : ')
        if monto == '':
            break
        try:
            monto = int(monto)
            if monto <= loginDatos[currentUser['user']]["balance"]:
                loginDatos[currentUser['user']]["balance"] -= monto
                mensaje(f"El monto fue debitado de su cuenta. Saldo total {loginDatos[currentUser['user']]['balance']}")
                break
            else:
                mensaje(f"El monto del retiro es mayor al saldo de su cuenta. Saldo total {loginDatos[currentUser['user']]['balance']}")
        except:
            mensaje('El monto debe ser un importe entero. Reintente')

def balance() ->None:
    """Muestra el balance por pantalla
    
    Return : None
    """
    os.system('clear')
    print('Balance')
    print('-------')
    print('')
    mensaje(f"El monto de su cuenta es de : {loginDatos[currentUser['user']]['balance']}")
    

def transfer() -> None:
    """Disminuye el valor del balance según lo ingresado
    Valida que se ingrese un entero
    Sale de la funcion si no se ingresa nada
    
    Return : None
    """
    while True:
        os.system('clear')
        print('Transferencias')
        print('--------------')
        monto =   input('Ingrese el monto a transferir   : ')
        destino = input('Ingrese el usuario destinatario : ')
        if monto == '':
            break
        try:
            monto = int(monto)
            if monto <= loginDatos[currentUser['user']]["balance"]:
                if destino in loginDatos :
                    loginDatos[currentUser['user']]["balance"] -= monto
                    loginDatos[destino]["balance"] += monto
                    mensaje(f"El monto fue debitado de su cuenta y acreditado al usuario de destino.")
                    break
                else:
                    mensaje('El usuario de destino no existe. Verifique.')
            else:
                mensaje(f"El monto de la transferencia es mayor al saldo de su cuenta. Saldo total {loginDatos[currentUser['user']]['balance']}")
        except:
            mensaje('El monto debe ser un importe entero. Reintente')

def logout() ->None:
    """ Cambia el estado del elemento login a False
        Cambia el usuario a ""
    """

    currentUser['user'] = ''
    mensaje('Sesión cerrada.')
    
def customQuit() -> None:
    grabaDatos('datos.csv')
    os.system('clear')
    exit()
    
def main() -> None:
    """ Arma menú de la aplicacion

    Keyword arguments: None

    Return: 
    """
    while True:

        opc_dict={
            "1":login,
            "2":deposits,    
            "3":widthdraws,  
            "4":balance,
            "5":transfer,
            "6":logout,  
            "7":customQuit    
            }
        
        os.system('clear')
        
        print(f"Sistema Bancario - Usuario {currentUser['user'].capitalize()}")
        print( '----------------   -------')
        print()
        print('1- Loggin      ')
        print('2- Deposits    ')
        print('3- Widthdraws  ')
        print('4- View Balance')
        print('5- Transfer    ')
        print('6- Logout      ')
        print('7- Quit        ')
        
        opcion = input('Ingrese la opción deseada :')
        
        if opcion in opc_dict:
            if currentUser['user'] != '':
                opc_dict[opcion]()
            else:
                if opcion != '1' and opcion != '7':
                    mensaje("Debe loguearse entes de realizar cualquier operación.")
                else:    
                    opc_dict[opcion]()
                    
        else:
            mensaje("Opción no válida. Reintente.")

 
loginDatos = cargaDatos('datos.csv')

currentUser = {'user':''}


main()