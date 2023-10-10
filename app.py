from cryptography.fernet import Fernet
import sqlite3
from tkinter import *
import random
from tkinter import messagebox
import os

# Contraseña Maestra
m_password = ""

# MyFernet (Será configurado como Fernet(key))
my_fernet = ""

# Configurando la ventana de Tkinter
root = Tk()
root.geometry("300x400")
root.title("Gestor/Generador de Contraseñas")
root.iconbitmap('/icon_icon.ico')

# Marcos invisibles para el programa
main_frame = Frame(root, padx=5, pady=5)
secondary_frame = Frame(root, padx=5, pady=5)
rbutton_frame = Frame(root, padx=5, pady=5)
output_frame = Frame(root, padx=5, pady=5)
bottom_bar = Frame(root, padx=5, pady=5)

main_frame.pack(padx=20, pady=0)
secondary_frame.pack(padx=20, pady=20)
rbutton_frame.pack(padx=10, pady=0)
output_frame.pack(padx=15, pady=5)
bottom_bar.pack(side=BOTTOM)

# Etiquetas
title = Label(main_frame, text="Generador de Contraseñas")
title.pack(padx=20, pady=0)

length = Label(secondary_frame, text="Longitud de la Contraseña (2-20):")
length.grid(row=0, column=0)

length_entry = Entry(secondary_frame)
length_entry.grid(row=0, column=1)

# Función para encriptar y desencriptar el archivo .db
def encriptar_db():
    with open('pw.db', 'rb') as to_encrypt:
        data = to_encrypt.read()
        data = my_fernet.encrypt(data)
        with open('pw.db', "wb") as encrypt:
            encrypt.write(data)

def desencriptar_db():
    with open('pw.db', 'rb') as to_decrypt:
        data = to_decrypt.read()
        data = my_fernet.decrypt(data)
        with open('pw.db', 'wb') as decrypt:
            decrypt.write(data)

# Función para guardar la contraseña maestra
def guardar_contraseña_maestra():
    # Generar una clave maestra para escribir
    with open('key.key', 'wb') as f:
        key = Fernet.generate_key()
        global my_fernet
        my_fernet = Fernet(key)
        f.seek(0)
        f.write(key)

    # Escribir la contraseña maestra codificada
    with open('pw.txt', 'wb') as f:
        f.seek(0)
        global m_password
        m_password = contraseña_maestra.get()
        contraseña_escrita = m_password.encode('utf-8')
        contraseña_escrita = my_fernet.encrypt(contraseña_escrita)
        f.write(contraseña_escrita)
    First_time.destroy()
    root.deiconify()
    encriptar_db()

# Comprobar si es la primera vez que se ejecuta el programa
with open('firstrun.txt', 'a+') as f:
    f.seek(0)
    f_contents = f.read()
    if f_contents == '1':
        with open('key.key', 'rb') as kf:
            kf.seek(0)
            kf_contents = kf.read()
            key = kf_contents
            my_fernet = Fernet(key)

        # Obtener la Contraseña Maestra
        with open('pw.txt', 'rb') as pf:
            pf.seek(0)
            pf_contents = pf.read()
            pf_contents = my_fernet.decrypt(pf_contents)
            pf_contents = pf_contents.decode('utf-8')
            m_password = pf_contents
    else:
        root.withdraw()
        f.seek(0)
        f.write('1')
        db = sqlite3.connect('pw.db')
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE passwords (
        app_id VARCHAR [255],
        username_email VARCHAR [255],
        password VARCHAR [255])
        ''')
        db.commit()
        db.close()

        # Ventana emergente para la primera ejecución
        First_time = Toplevel()
        First_time.title('Configuración')
        First_time.geometry('250x140')
        First_time.iconbitmap('./icon_icon.ico')

        # Configurar un marco de etiqueta para los campos de entrada
        labelframe = LabelFrame(
            First_time, text="Establecer una contraseña maestra para todas tus contraseñas.")
        labelframe.pack(fill="both", expand="yes")
        button_frame = Frame(First_time)
        button_frame.pack()

        # Campo de entrada para la contraseña maestra
        contraseña_maestra = Entry(labelframe, width=25)
        contraseña_maestra.pack()

        # Botón de envío
        AddButton = Button(
            button_frame, text='Establecer Contraseña Maestra', command=guardar_contraseña_maestra)
        AddButton.pack()

# Función para abrir el Cuaderno de Contraseñas
def Cuaderno_Contraseñas():
    cuaderno = Toplevel()
    cuaderno.title('Cuaderno de Contraseñas')
    cuaderno.geometry('390x700')
    cuaderno.iconbitmap('icon_icon.ico')

    # Función para recargar el Cuaderno de Contraseñas
    def recargar_cuaderno():
        cuaderno.destroy()
        Cuaderno_Contraseñas()

    # Función para agregar y eliminar contraseñas
    def agregar_contraseña():

        def guardar_contraseña():
            desencriptar_db()
            db = sqlite3.connect('pw.db')
            cursor = db.cursor()
            cursor.execute("INSERT INTO passwords VALUES (:App, :Usuario, :Contraseña)",
                           {'App': app_id_e.get(),
                            'Usuario': username_e.get(),
                            'Contraseña': password_e.get()
                            })
            db.commit()
            db.close()
            encriptar_db()
            alerta('Información', 'Contraseña guardada en el Cuaderno de Contraseñas')
            a_pass.destroy()
            recargar_cuaderno()

        a_pass = Toplevel()
        a_pass.title('Agregar Contraseña')
        a_pass.geometry('300x200')
        a_pass.iconbitmap('icon_icon.ico')

        pw_add_frame = LabelFrame(
            a_pass, text='Agregar Contraseña', padx=10, pady=10)
        pw_add_frame.pack(padx=5, pady=5)

        another_buttn_frame = Frame(a_pass, padx=10, pady=10)
        another_buttn_frame.pack(padx=0, pady=15)

        app_id = Label(pw_add_frame, text="Nombre de la Aplicación: ")
        app_id.grid(row=0, column=0)
        app_id_e = Entry(pw_add_frame)
        app_id_e.grid(row=0, column=1)

        username = Label(pw_add_frame, text="Nombre de Usuario/Email: ")
        username.grid(row=1, column=0)
        username_e = Entry(pw_add_frame)
        username_e.grid(row=1, column=1)

        password_label = Label(pw_add_frame, text='Contraseña: ')
        password_label.grid(row=2, column=0)

        password_e = Entry(pw_add_frame)
        password_e.grid(row=2, column=1)

        # Botón de envío
        Add_record_bttn = Button(
            another_buttn_frame, text="Agregar Contraseña", command=guardar_contraseña)
        Add_record_bttn.pack()

    def eliminar_contraseña():
        def eliminar_contraseña_db():
            desencriptar_db()
            db = sqlite3.connect('pw.db')
            cursor = db.cursor()
            cursor.execute("DELETE FROM passwords WHERE app_id = :app", {
                'app': app_name_delete.get()
            })
            db.commit()
            db.close()
            encriptar_db()
            alerta('Información', 'Contraseña eliminada')
            a_pass.destroy()
            recargar_cuaderno()

        a_pass = Toplevel()
        a_pass.title('Eliminar Contraseña')
        a_pass.geometry('300x200')
        a_pass.iconbitmap('icon_icon.ico')

        pw_add_frame = LabelFrame(
            a_pass, text='Eliminar Contraseña', padx=10, pady=10)
        pw_add_frame.pack(padx=5, pady=5)

        another_buttn_frame = Frame(a_pass, padx=10, pady=10)
        another_buttn_frame.pack(padx=0, pady=15)

        app_name = Label(pw_add_frame, text="Nombre de la Aplicación a eliminar: ")
        app_name.grid(row=0, column=0)
        app_name_delete = Entry(pw_add_frame)
        app_name_delete.grid(row=0, column=1)

        # Botón de envío
        Add_record_bttn = Button(
            another_buttn_frame, text="Eliminar", command=eliminar_contraseña_db)
        Add_record_bttn.pack()

    # Crear un marco de etiquetas para mostrar la tabla
    db_frame = LabelFrame(
        cuaderno, text="Contraseñas:")
    db_frame.pack(fill="both", expand="yes")

    # Crear otro marco para albergar los botones de agregar y eliminar
    buttn_frame = Frame(cuaderno, padx=10, pady=10)
    buttn_frame.pack(padx=5, pady=25)

    # Crear etiquetas para las columnas
    etiqueta_app_id = Label(db_frame, text="Nombre de la Aplicación")
    etiqueta_app_id.grid(row=0, column=1)

    etiqueta_usuario = Label(db_frame, text="Nombre de Usuario/Email")
    etiqueta_usuario.grid(row=0, column=2)

    etiqueta_contraseña = Label(db_frame, text="Contraseña")
    etiqueta_contraseña.grid(row=0, column=3)

    # Acceder a la base de datos
    desencriptar_db()
    db = sqlite3.connect('pw.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM passwords")

    # Mostrar la tabla de la base de datos
    i = 1
    for contraseña_sql in cursor:
        for j in range(len(contraseña_sql)):
            numero_linea = str(i)
            numero_linea = numero_linea + ". "
            l = Label(db_frame, text=numero_linea)
            l.grid(row=i, column=0)
            e = Entry(db_frame, width=20, fg='blue')
            u = j + 1
            e.grid(row=i, column=u)
            e.insert(END, contraseña_sql[j])
        i = i+1
    encriptar_db()

    # Crear botones para agregar y eliminar
    agregar_registro = Button(buttn_frame, text='Agregar Contraseña', command=agregar_contraseña)
    agregar_registro.grid(row=0, column=0)

    eliminar_registro = Button(
        buttn_frame, text='Eliminar Contraseña', command=eliminar_contraseña)
    eliminar_registro.grid(row=0, column=1)

# Función para abrir la página de Configuración
def Configuración():
    configuracion = Toplevel()
    configuracion.title('Configuración')
    configuracion.geometry('300x300')
    configuracion.iconbitmap('icon_icon.ico')

    marco_cambio_contraseña = LabelFrame(
        configuracion, text="Cambiar Contraseña Maestra", padx=10, pady=10)
    marco_cambio_contraseña.pack(padx=10, pady=10)

    marco_botones_configuracion = Frame(configuracion)
    marco_botones_configuracion.pack(padx=10, pady=20)

    def cambiar_contraseña_maestra():
        with open('pw.txt', 'wb') as f:
            f.seek(0)
            global m_password
            m_password = nueva_contraseña_maestra.get()
            contraseña_escrita = m_password.encode('utf-8')
            contraseña_escrita = my_fernet.encrypt(contraseña_escrita)
            f.write(contraseña_escrita)
            alerta('Información', 'La Contraseña Maestra ha sido cambiada')

    nueva_contraseña_maestra = Entry(marco_cambio_contraseña)
    nueva_contraseña_maestra.pack()

    cambiar_contraseña_maestra_buttn = Button(marco_botones_configuracion,
                                               text="Cambiar Contraseña Maestra", command=cambiar_contraseña_maestra)
    cambiar_contraseña_maestra_buttn.pack()

# Crear una función para autenticación
def Autenticación1():

    # Crear ventana Tkinter
    Autenticar = Toplevel()
    Autenticar.title('Autenticación')
    Autenticar.geometry('150x150')
    Autenticar.iconbitmap('icon_icon.ico')

    # Crear componentes de la ventana
    marco_autenticar = LabelFrame(
        Autenticar, text="Ingrese la Contraseña Maestra")
    marco_autenticar.pack(fill="both", expand="yes")
    marco_botones_autenticar = Frame(marco_autenticar)
    marco_botones_autenticar.pack()

    # Campo de entrada para la contraseña
    contraseña_maestra_entry = Entry(marco_autenticar, width=25)
    contraseña_maestra_entry.pack()

    # Función de autenticación real
    def AutenticaciónReal1():
        entrada_contraseña = contraseña_maestra_entry.get()
        if entrada_contraseña == m_password:
            Autenticar.destroy()
            Cuaderno_Contraseñas()
        else:
            alerta('Contraseña Incorrecta', 'La contraseña es incorrecta', tipo='warning')

    Botón_Autenticar = Button(
        marco_botones_autenticar, text='Autenticar', command=AutenticaciónReal1)
    Botón_Autenticar.pack()

# Crear una función de autenticación similar para la página de Configuración
def Autenticación2():

    # Crear ventana Tkinter
    Autenticar = Toplevel()
    Autenticar.title('Autenticación')
    Autenticar.geometry('150x150')
    Autenticar.iconbitmap('icon_icon.ico')

    # Crear componentes de la ventana
    marco_autenticar = LabelFrame(
        Autenticar, text="Ingrese la Contraseña Maestra")
    marco_autenticar.pack(fill="both", expand="yes")
    marco_botones_autenticar = Frame(marco_autenticar)
    marco_botones_autenticar.pack()

    # Campo de entrada para la contraseña
    contraseña_maestra_entry = Entry(marco_autenticar, width=25)
    contraseña_maestra_entry.pack()

    # Función de autenticación real
    def AutenticaciónReal2():
        entrada_contraseña = contraseña_maestra_entry.get()
        if entrada_contraseña == m_password:
            Autenticar.destroy()
            Configuración()
        else:
            alerta('Contraseña Incorrecta', 'La contraseña es incorrecta', tipo='warning')

    Botón_Autenticar = Button(
        marco_botones_autenticar, text='Autenticar', command=AutenticaciónReal2)
    Botón_Autenticar.pack()

# Botones de la barra inferior
Botón_Cuaderno_Contraseñas = Button(
    bottom_bar, text="Cuaderno de Contraseñas", command=Autenticación1)
Botón_Cuaderno_Contraseñas.grid(row=0, column=0)

# Botón de Configuración
Botón_Configuración = Button(bottom_bar, text="Configuración", command=Autenticación2)
Botón_Configuración.grid(row=1, column=0)

# Créditos
Créditos = Label(bottom_bar, text="Hecho por Santiago")
Créditos.grid(row=2, column=0)

# Función para mostrar una alerta
def alerta(título, mensaje, tipo='info'):
    if tipo not in ('error', 'warning', 'info'):
        raise ValueError('Tipo de alerta no soportado.')

    método_mostrar = getattr(messagebox, 'show{}'.format(tipo))
    método_mostrar(título, mensaje)

# Función para generar una contraseña
def generar_contraseña():

    # Obtener el valor del campo de entrada length_entry
    valor_length_entry = length_entry.get()

    # Verificar si el valor no está vacío y es numérico
    if valor_length_entry.strip() and valor_length_entry.isdigit():
        longitud_contraseña = int(valor_length_entry)
        caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZADEFKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789&{([-_@)]}=+*$%!?&{([-_@)]}=+*$%!?"
        contraseña_generada = ""
        for x in range(0, longitud_contraseña):
            contraseña_generada += str(random.choice(caracteres))

        def guardar_contraseña_principal():
            desencriptar_db()
            db = sqlite3.connect('pw.db')
            cursor = db.cursor()
            cursor.execute("INSERT INTO passwords VALUES (:App, :Usuario, :Contraseña)",
                        {'App': app_id_entry.get(),
                            'Usuario': usuario_input.get(),
                            'Contraseña': output_e.get()
                            })
            db.commit()
            db.close()
            encriptar_db()
            alerta('Información', 'Contraseña guardada en el Cuaderno de Contraseñas')

    else:
        # Mostrar un mensaje de error o manejar la situación de otra manera
        alerta('Error', 'Ingrese una longitud de contraseña válida', tipo='error')

    etiqueta_app_id = Label(output_frame, text="Nombre de la Aplicación: ")
    etiqueta_app_id.grid(row=1, column=0)
    app_id_entry = Entry(output_frame)
    app_id_entry.grid(row=1, column=1)

    etiqueta_usuario = Label(output_frame, text="Nombre de Usuario/Email: ")
    etiqueta_usuario.grid(row=2, column=0)
    usuario_input = Entry(output_frame)
    usuario_input.grid(row=2, column=1)

    etiqueta_contraseña = Label(output_frame, text='Contraseña Generada: ')
    etiqueta_contraseña.grid(row=0, column=0)

    output_e = Entry(output_frame)
    output_e.insert(END, contraseña_generada)
    output_e.grid(row=0, column=1)

    # Copiar automáticamente la contraseña generada
    root.clipboard_clear()
    root.clipboard_append(contraseña_generada)

    # Crear el botón de guardar
    guardar_contraseña_button = Button(
        output_frame, text="Guardar Contraseña", command=guardar_contraseña_principal)
    guardar_contraseña_button.grid(row=3, column=1)
    root.geometry("300x500")

# Botón para generar una contraseña
botón_generar_contraseña = Button(
    rbutton_frame, text="Generar Contraseña", command=generar_contraseña)
botón_generar_contraseña.grid(row=0, column=0)

# Texto debajo del botón para indicar la copia automática
texto_generar_contraseña = Label(
    rbutton_frame, text="El texto se copiará automáticamente al portapapeles.")
texto_generar_contraseña.grid(row=1, column=0)

# Iniciar la ventana de Tkinter
root.mainloop()