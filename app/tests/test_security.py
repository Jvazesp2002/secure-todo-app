import pytest
from models import User, Task

# Prueba para verificar que un usuario no puede acceder a las tareas de otro usuario
def test_user_cannot_see_others_tasks(client, db_session):
    # 1. Creamos dos usuarios distintos
    user_a = User(id=10, username="user_a", password_hash="hash1")
    user_b = User(id=20, username="user_b", password_hash="hash2")
    db_session.add_all([user_a, user_b])
    db_session.commit()

    # 2. El Usuario B tiene una tarea privada
    task_b = Task(id=50, title="Secreto de B", user_id=user_b.id)
    db_session.add(task_b)
    db_session.commit()

    # 3. Forzamos la sesión como Usuario A
    with client.session_transaction() as sess:
        sess['user_id'] = user_a.id
        sess['_fresh'] = True

    # 4. Usuario A intenta acceder a la tarea de Usuario B
    response = client.get(f'/tasks/{task_b.id}', follow_redirects=True)

    # 5. VERIFICACIÓN DE SEGURIDAD
    # El servidor debería responder 403 (Prohibido) o 404 (No encontrado)
    # pero NUNCA debería mostrar el título de la tarea del otro usuario.
    assert response.status_code in [403, 404]
    assert b"Secreto de B" not in response.data