import bcrypt

password = b'1234567891'
hash_resultado = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
print(hash_resultado)