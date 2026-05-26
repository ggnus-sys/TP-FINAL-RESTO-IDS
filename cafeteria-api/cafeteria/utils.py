import bcrypt

def hashear_password(password: str) -> str:
    """Genera un hash bcrypt del password en texto plano."""
    hash_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hash_bytes.decode('utf-8')


def verificar_password(password: str, password_hash: str) -> bool:
    """Compara un password en texto plano contra un hash bcrypt."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except (ValueError, TypeError):
        return False