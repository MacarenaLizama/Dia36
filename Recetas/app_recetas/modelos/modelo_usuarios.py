from app_recetas.config.mysqlconnection import connectToMySQL
from app_recetas import EMAIL_REGEX, BASE_DE_DATOS
from flask import flash

class Usuario:
    def __init__( self, data ):
        self.id = data ['id']
        self.nombre = data ['nombre']
        self.apellido = data ['apellido']
        self.email = data ['email']
        self.password = data ['password']
        self.fecha_creacion = data ['fecha_creacion']
        self.fecha_actualizacion = data ['fecha_actualizacion']

    @classmethod
    def obtener_uno_con_email( cls , data):
        query=  """
                SELECT *
                FROM usuarios
                WHERE email=%(email)s;
                """
        resultado = connectToMySQL(BASE_DE_DATOS).query_db( query, data)
        if len(resultado) == 0:
            return None
        else:
            return Usuario(resultado[0])
    
    @classmethod
    def crear_uno(cls, data):
        query=  """
                INSERT INTO usuarios (nombre, apellido, email, password)
                VALUES  (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
                """
        usuario_id= connectToMySQL(BASE_DE_DATOS).query_db( query,data )
        return usuario_id

    @staticmethod
    def validar_registro( data, usuario_existe ):
        es_valido = True
        if len( data['nombre']) < 2:
            es_valido = False
            flash("Se requiere un nombre de al menos dos caracteres", "error_nombre")
        if len( data['apellido']) < 2:
            es_valido = False
            flash("Se requiere un apellido de al menos dos caracteres", "error_apellido")
        if not EMAIL_REGEX.match( data['email']):
            es_valido=False
            flash("Ingrese un email válido", "error_email")
        if data['password'] != data['confirmacion_password']:
            es_valido = False
            flash("Las contraseñas no coinciden", "error_password")
        if usuario_existe != None:
            es_valido = False
            flash("Este email ya esta en uso", "error_email")

        return es_valido
    
