import requests
import base64

# --- CONFIGURACIÓN ---
API_BASE = "https://fibhplr.fundanetsuite.com/fundanetapi"
USER = "Fundanet"
PASSWORD = "cLv.140492"  # Se recomienda en la práctica usar variables de entorno

# --- OBTENER TOKEN ---
def obtener_token():
    url = f"{API_BASE}/api/autorizacion"
    credenciales = f"{USER}:{PASSWORD}"
    token = base64.b64encode(credenciales.encode()).decode()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.text.strip('"')  # el token viene como string entre comillas
    else:
        print(f"❌ Error al obtener token: {response.status_code}")
        print(response.text)
        return None

# --- CONSULTAR EMPLEADOS ---
def consultar_empleados(token):
    url = f"{API_BASE}/api/rrhh/empleados"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Empleados recibidos:")
        for emp in data.get("Elementos", []):
            print(f" - {emp.get('Nombre')} {emp.get('Apellido1')} ({emp.get('IdEmpleado')})")
    else:
        print(f"❌ Error al consultar empleados: {response.status_code}")
        print(response.text)

# --- FLUJO PRINCIPAL ---
if __name__ == "__main__":
    token = obtener_token()
    if token:
        consultar_empleados(token)
