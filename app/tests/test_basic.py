def test_register_page_accessible(client):
    """Verifica que la página de registro carga correctamente sin estar logueado."""
    response = client.get('/register')
    
    # Verificamos que responda 200 OK
    assert response.status_code == 200
    # Verificamos que contenga algo característico del formulario
    assert b"Registrate" in response.data or b"password" in response.data