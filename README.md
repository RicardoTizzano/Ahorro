 Ahorro

 Sistema simple "bancario" que permite las siguientes funcionalidades
 Almacena los usuarios, pass (no tiene algoritmo de seguridad), status y balance
 en un archivo .csv y guarda backup cada vez que se sale del sistema y almacena la nueva información en 
 el archivo datos.csv

 Login         : Realiza control con clave
                 Si el usuario no existe permite darlo de alta. 
                 Verifica la clave por comparación
                 Inicia el usuario con un saldo de 2000
                 Administra múltiples usuarios
                 Bloquea al usuario después de tres intentos fallidos de la clave
    
 Depósitos     : Permite hacer depósitos
 Retiros       : Permite realizar retiros. Valida que no se pueda retirar más que el saldo actual
 Consulta      : Permite consultar el saldo de la cuenta del usuario
 Tranferencias : Permite realizar transferencias entre cuentas a diferentes usuarios
 Logout        : Permite cerrar la sesión del usuario
 Cambio de 
 idioma        : Permite el cambio de idioma del sistema entre varios elejidos al              azar

 Quit          : Finaliza el programa, actualiza la información el .csv y backapea el último archivo

