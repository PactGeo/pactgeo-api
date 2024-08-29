from passlib.context import CryptContext

# Configuración del contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro para la contraseña proporcionada.

    Args:
        password (str): La contraseña en texto plano que se desea hashear.

    Returns:
        str: El hash seguro de la contraseña.
    """
    return pwd_context.hash(password)
