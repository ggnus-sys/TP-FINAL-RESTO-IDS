import requests
from ..constants import API_BASE_URL




#services/auth.py tiene las funciones que hacen los requests para la comunicación con la API
#el proposito de esto es facilitar el proceso de los datos y solo tener que leer el "ok" para verificar que las cosas se hicieron bien

 
def login_api(email, password):
    try:
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f'{API_BASE_URL}/login', json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return {'ok': True, 'token': data['token'], 'usuario': data['usuario']}
        else:
            data = response.json()
            mensajes = [e.get('description') or e.get('message') for e in data.get('errors', [])]
            return {'ok': False, 'errores': mensajes}


    except Exception as e:
        return {'ok': False, 'errores': [f'No se pudo conectar con la API: {e}']}
    

def register_api (nombre, apellido, email, password):
    try:
        payload = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "password": password
        }
        response = requests.post(f'{API_BASE_URL}/register', json=payload)

        if response.status_code == 201:
            data = response.json()
            return {'ok': True, "usuario": data}
        else:
            data = response.json()
            mensajes = [e.get('description') or e.get('message') for e in data.get('errors', [])]
            return {'ok': False, 'errores': mensajes}

    except Exception as e:
        return {'ok': False, 'errores': [f'No se pudo conectar con la API: {e}']}
    

