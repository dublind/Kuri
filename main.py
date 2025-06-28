import oracledb
import time
from datetime import date
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
def pagos(id_usuario, tipo_paseo):
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO pagos (usuario_id, tipo_paseo)
        VALUES (:usuario_id, :tipo_paseo)
    """, {
        'usuario_id': id_usuario,
        'tipo_paseo': tipo_paseo
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
                print("3. registrar perro")
                print("4. Salir")
                print("Seleccione una opción:")
                opcion_submenu = input()
                if opcion_submenu == "1":
                    print("¡Vamos a pasear a tu perro! 🐕")
                    time.sleep(1)
                    print("Recuerda entregarnos a tu perro con correa para el paseo!.")
                    print("cual es el nombre de tu perro?")
                    nombre_perro = input()
                    cursor = conexion.cursor()
                    cursor.execute("""
                        SeLECT * FROM perros WHERE nombre = :nombre_perro
                    """, {
                        'nombre_perro': nombre_perro
                    })
                    perro_encontrado = cursor.fetchone()
                    cursor.close()
                    if perro_encontrado:
                        print(f"Tu perro {perro_encontrado[1]} está listo para el paseo!")
                        #creacion de un submenu de precios de paseos
                        print("Seleccione el tipo de paseo:")
                        print("1. Paseo corto (30 minutos) - $10")
                        print("2. Paseo largo (1 hora) - $20")
                        print("3. Paseo especial (2 horas) - $30")
                        tipo_paseo = input()
                        if tipo_paseo == "1":
                            print("Has seleccionado un paseo corto (30 minutos) - $10")
                            pagos(usuario_encontrado[0], 10)
                        elif tipo_paseo == "2":
                            print("Has seleccionado un paseo largo (1 hora) - $20")
                            pagos(usuario_encontrado[0], 20)
                        elif tipo_paseo == "3":
                            print("Has seleccionado un paseo especial (2 horas) - $30")
                            pagos(usuario_encontrado[0], 30)
                    else:
                        print("No se encontró un perro con ese nombre. Asegúrate de que esté registrado.")
                        time.sleep(1)
                        print("Por favor, regístralo primero.")
                elif opcion_submenu == "2":
                    print(f"Perfil de {usuario_encontrado[1]} {usuario_encontrado[2]}:")
                    print(f"Correo: {usuario_encontrado[4]}")
                    print(f"Teléfono: {usuario_encontrado[5]}")
                    time.sleep(1)
                elif opcion_submenu == "3":
                    print("Ingrese el nombre de su perro:")
                    nombre_perro = input()
                    print("Ingrese la raza de su perro:")
                    raza_perro = input()
                    print("Ingrese la edad de su perro:")
                    edad_perro = input()
                    print("Ingrese peso del perro:")
                    peso_perro = input()
                    cursor = conexion.cursor()
                    cursor.execute("""
                        INSERT INTO perros (nombre, raza, edad, peso, usuario_id)
                        VALUES (:nombre, :raza, :edad, :peso, :usuario_id)
                    """, {
                        'nombre': nombre_perro,
                        'raza': raza_perro,
                        'edad': edad_perro,
                        'peso': peso_perro,
                        'usuario_id': usuario_encontrado[0]
                    })
                    conexion.commit()
                    cursor.close()
                    print(f"Perro {nombre_perro} registrado exitosamente. {usuario_encontrado[1]} ahora podemos.")
                elif opcion_submenu == "4":
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