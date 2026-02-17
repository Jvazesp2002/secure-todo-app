import pytest
import time
import requests

def test_nginx_rate_limiting():
    url = "https://nginx/login"
    success_count = 0
    blocked_count = 0
    
    # Enviamos 10 peticiones rápidamente
    for _ in range(15):
        response = requests.get(url, verify=False)  # Ignorar certificado para pruebas
        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 503 or response.status_code == 429:
            blocked_count += 1
    
    print(f"Exitosas: {success_count}, Bloqueadas: {blocked_count}")
    # Deberia bloquear alguna petición
    assert blocked_count > 0 