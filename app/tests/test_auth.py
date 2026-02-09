def test_register_user(client):
    # Registrar un nuevo usuario
    response = client.post("/register", data={
        "username": "testuser",
        "password": "testpass"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Usuario creado correctamente" in response.data
    
def test_login_success(client):
    # Registrar un nuevo usuario
    client.post("/register", data={
        "username": "testuser",
        "password": "testpass"
    })
    
    response = client.post("/login", data={
        "username": "testuser",
        "password": "testpass"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Dashboard" in response.data
    
def test_login_failure(client):
    response = client.post("/login", data={
        "username": "nonexistent",
        "password": "wrongpass"
    }, follow_redirects=True)
    
    assert b"Credenciales incorrectas" in response.data