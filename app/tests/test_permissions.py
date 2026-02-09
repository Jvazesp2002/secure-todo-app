from models import User, Task, SessionLocal
from werkzeug.security import generate_password_hash

def create_user(username, admin=False):
    db = SessionLocal()
    user = User(
        username=username,
        password_hash=generate_password_hash("1234"),
        is_admin=admin
    )
    db.add(user)
    db.commit()
    return user

def login(client, username):
    return client.post("/login", data={
        "username": username,
        "password": "1234"
    }, follow_redirects=True)
    
def test_admin_can_see_all_tasks(client):
    admin = create_user("admin", admin=True)
    user1 = create_user("user1")
    user2 = create_user("user2")
    
    db = SessionLocal()
    db.add(Task(title="Tarea User1", description="Desc User1", user_id=user1.id))
    db.add(Task(title="Tarea User2", description="Desc User2", user_id=user2.id))
    db.add(Task(title="Tarea Admin", description="Desc Admin", user_id=admin.id))   
    db.commit()
    
    login(client, "admin")
    response = client.get("/tasks")
    
    assert b"Tarea User1" in response.data
    assert b"Tarea User2" in response.data
    assert b"Tarea Admin" in response.data
    
def test_user_can_only_see_own_tasks(client):
    user1 = create_user("user1")
    user2 = create_user("user2")
    
    db = SessionLocal()
    db.add(Task(title="Tarea User1", description="Desc User1", user_id=user1.id))
    db.add(Task(title="Tarea User2", description="Desc User2", user_id=user2.id))
    db.add(Task(title="Tarea Admin", description="Desc Admin", user_id=user1.id))
    db.commit()
    
    login(client, "user1")
    response = client.get("/tasks")
    
    assert b"Tarea User1" in response.data
    assert b"Tarea Admin" not in response.data
    assert b"Tarea User2" not in response.data
    
def test_user_cannot_delete_others_tasks(client):
    user1 = create_user("user1")
    user2 = create_user("user2")
    
    db = SessionLocal()
    task = Task(title="Tarea User2", description="Desc User2", user_id=user2.id)
    db.add(task)
    db.commit()
    
    login(client, "user1")
    response = client.post(f"/tasks/{task.id}/delete", follow_redirects=True)
    
    assert response.status_code in (403, 302)  # Puede ser un error de permiso o redirección