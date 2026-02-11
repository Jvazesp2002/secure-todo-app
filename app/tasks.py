from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from models import SessionLocal, Task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks")
@login_required
def list_tasks():
    db = SessionLocal()
    if current_user.is_admin:
        tasks = db.query(Task).all()
    else:
        tasks = db.query(Task).filter_by(user_id=current_user.id).all()
        
    return render_template("tasks.html", tasks=tasks)

@tasks_bp.route("/tasks/create", methods=["POST"])
@login_required
def create_task():
    title = request.form.get("title")
    description = request.form.get("description")

    if not title or not description:
        flash("El título y la descripción son obligatorios.")
        return redirect(url_for("tasks.list_tasks"))

    db = SessionLocal()

    task = Task(
        title=title,
        description=description,
        user_id=current_user.id
    )

    db.add(task)
    db.commit()

    return redirect(url_for("tasks.list_tasks"))

@tasks_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    db = SessionLocal()
    task = db.query(Task).get(task_id)

    if not task:
        flash("La tarea no existe")
        return redirect(url_for("tasks.list_tasks"))

    if task.user_id != current_user.id and not current_user.is_admin:
        flash("No tienes permiso para borrar esta tarea")
        return redirect(url_for("tasks.list_tasks"))

    db.delete(task)
    db.commit()

    flash("Tarea eliminada correctamente")
    return redirect(url_for("tasks.list_tasks"))