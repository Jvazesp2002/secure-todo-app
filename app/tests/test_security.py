def test_create_task_flow(client):
    """Test de integración: Login -> Crear Tarea -> Verificar persistencia."""
    # 1. Simular login (saltando CSRF para el test de unidad)
    with client.session_transaction() as sess:
        sess['user_id'] = 1 
    
    # 2. Crear tarea
    response = client.post('/tasks/create', data={
        'title': 'Auditar Servidor',
        'description': 'Revisar logs de Nginx'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Auditar Servidor" in response.data