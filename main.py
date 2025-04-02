import os
import json
from datetime import datetime

ARCHIVOS = {
    'individual': 'clientes_individual.json',
    'acompañado': 'clientes_acompañado.json',
    'grupo': 'clientes_grupo.json'
}

HABITACIONES = {
    'FAMILY ROOM': {
        'precio': 200,
        'capacidad': 4,
        'descripcion': """Cálida y confortable habitación decorada con un estilo vanguardista..."""
    },
    'SENCILLA': {
        'precio': 60,
        'capacidad': 1,
        'descripcion': """Amplia y confortable habitación decorada con un estilo vanguardista..."""
    },
    'DOBLE': {
        'precio': 120,
        'capacidad': 2,
        'descripcion': """Amplia y confortable habitación decorada con un estilo vanguardista..."""
    },
    'SUITE': {
        'precio': 300,
        'capacidad': 4,
        'descripcion': """Cálida y confortable habitación decorada con un estilo vanguardista..."""
    }
}

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_clientes(tipo):
    try:
        with open(ARCHIVOS[tipo], 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_clientes(tipo, datos):
    with open(ARCHIVOS[tipo], 'w') as f:
        json.dump(datos, f, indent=4)

def mostrar_menu_principal():
    limpiar_pantalla()
    print("""
    HOTEL LIDOTEL BOUTIQUE MARGARITA
    
    1. Nueva reservación
    2. Salir
    """)

def mostrar_menu_tipo_reserva():
    limpiar_pantalla()
    print("""
    TIPO DE RESERVACIÓN
    
    1. Individual
    2. Acompañado
    3. Grupo/Familia
    4. Atrás
    """)

def mostrar_menu_habitaciones():
    limpiar_pantalla()
    print("""
    TIPOS DE HABITACIONES
    """)
    for i, (tipo, info) in enumerate(HABITACIONES.items(), 1):
        print(f"{i}. {tipo} - ${info['precio']} por noche (Máx. {info['capacidad']} pers.)")
    print("\nSeleccione una opción:")

def mostrar_detalle_habitacion(tipo):
    limpiar_pantalla()
    print(f"\n{tipo} - ${HABITACIONES[tipo]['precio']} por noche (Máx. {HABITACIONES[tipo]['capacidad']} pers.)")
    print("\nDescripción:")
    print(HABITACIONES[tipo]['descripcion'])
    input("\nPresione Enter para continuar...")

def obtener_input_valido(mensaje, tipo='texto', min_len=1):
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print("Error: Este campo es obligatorio.")
            continue
        
        if tipo == 'numero':
            if valor.isdigit():
                return int(valor)
            print("Error: Debe ingresar un número válido.")
        elif tipo == 'email':
            if '@' in valor and '.' in valor:
                return valor
            print("Error: Ingrese un email válido (ejemplo@dominio.com).")
        elif tipo == 'telefono':
            if valor.isdigit() and len(valor) >= 7:
                return valor
            print("Error: El teléfono debe contener solo números (mínimo 7 dígitos).")
        elif tipo == 'cedula':
            if valor.isdigit() and len(valor) >= 6:
                return valor
            print("Error: La cédula debe contener solo números (mínimo 6 dígitos).")
        else:  # texto
            if valor.replace(" ", "").isalpha():
                return valor
            print("Error: Ingrese solo letras y espacios.")

def obtener_datos_persona():
    limpiar_pantalla()
    print("\nIngrese los datos:")
    
    nombre = obtener_input_valido("Nombre: ")
    apellido = obtener_input_valido("Apellido: ")
    cedula = obtener_input_valido("Número de cédula: ", 'cedula')
    email = obtener_input_valido("Email: ", 'email')
    telefono = obtener_input_valido("Número de teléfono: ", 'telefono')
    dias = obtener_input_valido("Cantidad de días de estadía: ", 'numero')
    
    return {
        'nombre': nombre,
        'apellido': apellido,
        'cedula': cedula,
        'email': email,
        'telefono': telefono,
        'dias': dias
    }

def seleccionar_habitacion():
    while True:
        mostrar_menu_habitaciones()
        opcion = input("Opción: ")
        
        if opcion.isdigit() and 1 <= int(opcion) <= len(HABITACIONES):
            tipo = list(HABITACIONES.keys())[int(opcion)-1]
            mostrar_detalle_habitacion(tipo)
            
            confirmar = input(f"\n¿Seleccionar la habitación {tipo}? (S/N): ").upper()
            if confirmar == 'S':
                return tipo
        else:
            print("Error: Opción inválida. Seleccione un número del 1 al 4.")

def calcular_costo(reserva, tipo_reserva):
    habitacion = HABITACIONES[reserva['habitacion']]
    precio_base = habitacion['precio']
    dias = reserva['dias']
    
    if tipo_reserva == 'individual':
        return precio_base * dias
    
    elif tipo_reserva == 'acompañado':
        return precio_base * dias
    
    elif tipo_reserva == 'grupo':
        total_personas = len(reserva['adultos']) + len(reserva.get('niños', []))
        
        if total_personas > 2:
            personas_extra = total_personas - 2
            costo_extra = personas_extra * 50
            return (precio_base + costo_extra) * dias
        else:
            return precio_base * dias

def mostrar_reserva(reserva, tipo_reserva):
    limpiar_pantalla()
    print("\nDETALLE DE RESERVA")
    
    if tipo_reserva == 'individual':
        persona = reserva['cliente']
        print(f"\nCliente: {persona['nombre']} {persona['apellido']}")
        print(f"Cédula: {persona['cedula']}")
        
    elif tipo_reserva == 'acompañado':
        cliente = reserva['cliente']
        acompañante = reserva['acompañante']
        
        print("\nCLIENTE PRINCIPAL:")
        print(f"Nombre: {cliente['nombre']} {cliente['apellido']}")
        
        print("\nACOMPAÑANTE:")
        print(f"Nombre: {acompañante['nombre']} {acompañante['apellido']}")
        
    elif tipo_reserva == 'grupo':
        adultos = reserva['adultos']
        niños = reserva.get('niños', [])
        
        print("\nADULTOS EN EL GRUPO:")
        for i, adulto in enumerate(adultos, 1):
            print(f"\nAdulto {i}:")
            print(f"Nombre: {adulto['nombre']} {adulto['apellido']}")
        
        if niños:
            print("\nNIÑOS EN EL GRUPO:")
            for i, niño in enumerate(niños, 1):
                print(f"\nNiño {i}:")
                print(f"Nombre: {niño['nombre']} {niño['apellido']}")
    
    habitacion = reserva['habitacion']
    precio_noche = HABITACIONES[habitacion]['precio']
    capacidad = HABITACIONES[habitacion]['capacidad']
    total = calcular_costo(reserva, tipo_reserva)
    
    print(f"\nHabitación: {habitacion} (Capacidad: {capacidad} personas)")
    print(f"Precio base por noche: ${precio_noche}")
    
    if tipo_reserva == 'grupo':
        total_personas = len(reserva['adultos']) + len(reserva.get('niños', []))
        if total_personas > 2:
            print(f"Cargo adicional por {total_personas-2} personas extra: ${50*(total_personas-2)}/noche")
    
    print(f"Total a pagar: ${total}")
    input("\nPresione Enter para continuar...")

def proceso_individual():
    clientes = cargar_clientes('individual')
    cliente = obtener_datos_persona()
    habitacion = seleccionar_habitacion()
    
    reserva = {
        'cliente': cliente,
        'habitacion': habitacion,
        'dias': cliente['dias'],
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    clientes.append(reserva)
    guardar_clientes('individual', clientes)
    mostrar_reserva(reserva, 'individual')

def proceso_acompañado():
    clientes = cargar_clientes('acompañado')
    cliente = obtener_datos_persona()
    acompañante = obtener_datos_persona()
    
    dias = cliente['dias']
    acompañante['dias'] = dias
    
    habitacion = seleccionar_habitacion()
    
    if HABITACIONES[habitacion]['capacidad'] < 2:
        print("\nError: La habitación seleccionada no tiene capacidad para 2 personas")
        input("Presione Enter para continuar...")
        return
    
    reserva = {
        'cliente': cliente,
        'acompañante': acompañante,
        'habitacion': habitacion,
        'dias': dias,
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    clientes.append(reserva)
    guardar_clientes('acompañado', clientes)
    mostrar_reserva(reserva, 'acompañado')

def obtener_datos_niño():
    print("\nIngrese los datos del niño:")
    nombre = obtener_input_valido("Nombre: ")
    apellido = obtener_input_valido("Apellido: ")
    edad = obtener_input_valido("Edad: ", 'numero')
    return {
        'nombre': nombre,
        'apellido': apellido,
        'edad': edad
    }

def proceso_grupo():
    clientes = cargar_clientes('grupo')
    
    num_adultos = obtener_input_valido("Cantidad de adultos en el grupo: ", 'numero')
    adultos = []
    for _ in range(num_adultos):
        adultos.append(obtener_datos_persona())
    
    dias = adultos[0]['dias']
    for adulto in adultos[1:]:
        adulto['dias'] = dias
    
    niños = []
    tiene_niños = input("¿Incluye niños? (S/N): ").upper()
    if tiene_niños == 'S':
        num_niños = obtener_input_valido("Cantidad de niños: ", 'numero')
        for _ in range(num_niños):
            niños.append(obtener_datos_niño())
    
    habitacion = seleccionar_habitacion()
    total_personas = num_adultos + len(niños)
    
    if HABITACIONES[habitacion]['capacidad'] < total_personas:
        print(f"\nError: La habitación seleccionada no tiene capacidad para {total_personas} personas")
        input("Presione Enter para continuar...")
        return
    
    reserva = {
        'adultos': adultos,
        'dias': dias,
        'habitacion': habitacion,
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if niños:
        reserva['niños'] = niños
    
    clientes.append(reserva)
    guardar_clientes('grupo', clientes)
    mostrar_reserva(reserva, 'grupo')

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Opción: ")
        
        if opcion == '1':
            while True:
                mostrar_menu_tipo_reserva()
                opcion_tipo = input("Opción: ")
                
                if opcion_tipo == '1':
                    proceso_individual()
                    break
                elif opcion_tipo == '2':
                    proceso_acompañado()
                    break
                elif opcion_tipo == '3':
                    proceso_grupo()
                    break
                elif opcion_tipo == '4':
                    break
                else:
                    print("Error: Opción inválida. Seleccione 1-4.")
        
        elif opcion == '2':
            print("Gracias por utilizar el sistema")
            break
        
        else:
            print("Error: Opción inválida. Seleccione 1 o 2.")

if __name__ == "__main__":
    for archivo in ARCHIVOS.values():
        if not os.path.exists(archivo):
            with open(archivo, 'w') as f:
                json.dump([], f)
    
    main()
