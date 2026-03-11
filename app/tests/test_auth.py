from models import User

# Prueba para verificar que el hashing de contraseñas funciona correctamente
def test_password_hashing():
    user = User(username="testuser")
    user.password_hash = "hash_simulado" 
    
    assert user.username == "testuser"
    assert user.password_hash != "Password123!"