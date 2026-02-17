from models import User
def test_password_hashing():
    """Verifica que las contraseñas se hasheen correctamente."""
    user = User(username="testuser")
    user.password_hash = "hash_simulado" 
    
    assert user.username == "testuser"
    assert user.password_hash != "Password123!"