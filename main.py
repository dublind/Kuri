import oracledb
import time

# Datos de conexión
usuario = "system"
contraseña = "Atom"
dsn = "localhost/xe"  # Cambia esto según tu base

# Conectar a la base de datos
conexion = oracledb.connect(
    user=usuario,
    password=contraseña,
    dsn=dsn
    )
#funcion para guardar datos de usuarios en script.sql
def guardar_datos_usuarios(nombre, apellido_p, apellido_m, correo, telefono, contrasella):
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nombre, apellido_p, apellido_m, correo, telefono, contrasella)
        VALUES (:nombre, :apellido_p, :apellido_m, :correo, :telefono, :contrasella)
    """, {
        'nombre': nombre,
        'apellido_p': apellido_p,
        'apellido_m': apellido_m,
        'correo': correo,
        'telefono': telefono,
        'contrasella': contrasella
    })
    conexion.commit()
    cursor.close()
# creacion de una app de paseo de perros
menu = True
while menu:
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    print("Seleccione una opción:")
    opcion = input()
    if opcion == "1":
        print("Ingrese su nombre de usuario:")
        nombre_usuario = input()
        print("Ingrese su contraseña:")
        contrasena_usuario = input()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM usuarios WHERE nombre = :nombre AND contrasella = :contrasena
        """, {
            'nombre': nombre_usuario,
            'contrasena': contrasena_usuario
        })
        usuario_encontrado = cursor.fetchone()
        cursor.close()
        if usuario_encontrado:
            print(f"Bienvenido, {usuario_encontrado[1]} {usuario_encontrado[2]}!")
            submenu = True
            while submenu:
                print("1. pasear a tu perro 🐶")
                print("2. Ver perfil")
                print("3. Salir")
                print("Seleccione una opción:")
                opcion_submenu = input()
                if opcion_submenu == "1":
                    print("¡Vamos a pasear a tu perro! 🐕")
                    time.sleep(1)
                    print("Recuerda entregarnos a tu perro con correa para el paseo.")
                    # Aquí podrías agregar más lógica para el paseo del perro
                elif opcion_submenu == "2":
                    print(f"Perfil de {usuario_encontrado[1]} {usuario_encontrado[2]}:")
                    print(f"Correo: {usuario_encontrado[4]}")
                    print(f"Teléfono: {usuario_encontrado[5]}")
                    time.sleep(1)
                elif opcion_submenu == "3":
                    submenu = False
                    print("Saliendo del menú de usuario...")
                    time.sleep(1)
        else:
            print("Nombre de usuario o contraseña incorrectos.")
    elif opcion == "2":
        print("Ingrese su nombre:")
        nombre = input()
        print("Ingrese su apellido paterno:")
        apellido_p = input()
        print("Ingrese su apellido materno:")
        apellido_m = input()
        print("Ingrese su correo electrónico:")
        correo = input()
        print("Ingrese su número de teléfono:")
        telefono = input()
        print("Ingrese su contraseña:")
        contrasella = input()
        guardar_datos_usuarios(nombre, apellido_p, apellido_m, correo, telefono, contrasella)
        print("Usuario registrado exitosamente.")
    elif opcion == "3":
        print("Saliendo de la aplicación...")
        menu = False
    else:
        print("Opción no válida. Por favor, intente de nuevo.")