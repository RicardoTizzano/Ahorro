from googletrans import Translator
import os
import csv
from datetime import datetime
import json


def mensaje(mensaje) -> None:
    """ Muestra mensaje por pantalla con una pausa
    
    Keyword arguments: Mensaje a mostrar
    argument -str- string del mensaje
    Return: None
    """
    print(traduceTexto(mensaje,idioma))
    input()

def display_en_columnas(idiomas):
    os.system('clear')
    
    elementos = list(idiomas.items())
    elementos_en_columnas = [elementos[i:i+4] for i in range(0, len(elementos), 4)]

    # Imprimir en cuatro columnas con tabulación
    for fila in elementos_en_columnas:
        for clave, valor in fila:
            print(f"{clave.ljust(1)} - {str(valor)[:14].ljust(14)}", end="    ")
        print()
    print()

def traduceTexto(texto, idioma_salida)->str:
    """Cambia a idioma_salida elegido el texto
    
    Keyword arguments:
    texto(str) : Texto a traducir
    idioma_salida(str) : Idioma al que traducir
    
    Return: texto traducido al idioma_salida
    """
    global idioma
        
    translator = Translator()
    traduccion = translator.translate(texto, src='es', dest=idioma_salida)
    return traduccion.text

def cambiaIdioma()->None:
    """Cambia el idioma del sistema
    
    Keyword arguments:
    idioma -- Elije de los idiomas disponibles en idiomas.json
    Return: return_description
    """
    global idioma
    
    with open('idiomas.json', 'r') as archivo:
        idiomas = json.load(archivo)
    display_en_columnas(idiomas)
    idiomaSalida = input(traduceTexto('Ingrese el idioma :',idioma))
    try:
        idiomas[idiomaSalida]
        if idiomaSalida != "":
            idioma = idiomaSalida
    except:
        return idioma
    
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
                mensaje('Hubo inconvenientes en la lectura de los datos. La información puede no estar actualizada',)
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
        print(f"{traduceTexto('Usuario',idioma)} : {usuario}")
        clave = input(traduceTexto('Ingrese su clave   :',idioma))
        claveControl = input(traduceTexto('Reingrese su clave :',idioma))
        if clave != claveControl:
            mensaje("Las claves no coinciden. Reintente",idioma)
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
        usuario  = input(traduceTexto('Ingrese el usuario :',idioma))
        if usuario == '':
            break
        if usuario.lower() in loginDatos :
            if loginDatos[usuario]['status'] == 'block':
                mensaje('Usuario bloqueado. Comuníquese con el banco.')
                exit()
            for i in range(3):
                os.system('clear')
                print(traduceTexto('Ingrese el usuario :' + usuario,idioma))
    
                clave = input(traduceTexto('Ingrese la clave   :',idioma))
                if clave == loginDatos[usuario]['pass']:
                    currentUser['user'] = usuario.lower()
                    return True

                else:
                    mensaje(f'Clave incorrecta. Quedan {2 - i } intentos. Presione una tecla para reintentar')

            loginDatos[usuario]['status'] = 'block'
            mensaje(f'Usuario bloqueado. Presione una tecla para seguir')

            break
        else:
            if input(traduceTexto('Usuario inexistente. Desea darlo de alta (s/n)? ',idioma).lower()) == 's':
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
        print(traduceTexto('Depósitos',idioma))
        print('---------')
        monto = input(traduceTexto('Ingrese el monto a depositar : ',idioma))
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
        print(traduceTexto('Retiros',idioma))
        print('-------')
        monto = input(traduceTexto('Ingrese el monto a retirar : ',idioma))
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
    print(traduceTexto('Balance',idioma))
    print('-------')
    print('')
    texto = traduceTexto('El monto de su cuenta es de :',idioma)
    mensaje(f"{texto} {loginDatos[currentUser['user']]['balance']}")
    

def transfer() -> None:
    """Disminuye el valor del balance según lo ingresado
    Valida que se ingrese un entero
    Sale de la funcion si no se ingresa nada
    
    Return : None
    """
    while True:
        os.system('clear')
        print(traduceTexto('Transferencias',idioma))
        print('--------------')
        monto =   input(traduceTexto('Ingrese el monto a transferir   : ',idioma))
        destino = input(traduceTexto('Ingrese el usuario destinatario : '),idioma)
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
    global idioma

    while True:

        opc_dict={
            "1":login,
            "2":deposits,    
            "3":widthdraws,  
            "4":balance,
            "5":transfer,
            "6":logout,  
            "7":cambiaIdioma,
            "8":customQuit    
            }
        
        os.system('clear')
        titulo = traduceTexto('Sistema Bancario - Usuario',idioma)
        print(f"{titulo} {currentUser['user'].capitalize()}")
        print( '----------------  ','-------', '-' * len(currentUser['user']))
        print()
        print(traduceTexto('1- Acceso         ',idioma))
        print(traduceTexto('2- Depositos      ',idioma))
        print(traduceTexto('3- Retiros        ',idioma))
        print(traduceTexto('4- Ver balance    ',idioma))
        print(traduceTexto('5- Transferencias ',idioma))
        print(traduceTexto('6- Cerrar sesión  ',idioma))
        print(traduceTexto('7- Cambia Idioma  ',idioma))
        print(traduceTexto('8- Salir          ',idioma))
        
        opcion = input(traduceTexto('Ingrese la opción deseada :',idioma))
        
        if opcion in opc_dict:
            if currentUser['user'] != '':
                opc_dict[opcion]()
            else:
                if opcion != '1' and opcion != '8' and opcion!='7':
                    mensaje("Debe loguearse entes de realizar cualquier operación.")
                else:    
                    opc_dict[opcion]()
                    
        else:
            mensaje("Opción no válida. Reintente.")

 
loginDatos = cargaDatos('datos.csv')

currentUser = {'user':''}

# Idioma por default
idioma = 'es'

main()