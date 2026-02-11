from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from models import SessionLocal, Task
from forms import TaskForm

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks")
@login_required
def list_tasks():
    db = TaskForm()
    db = SessionLocal()
    if current_user.is_admin:
        tasks = db.query(Task).all()
    else:
        tasks = db.query(Task).filter_by(user_id=current_user.id).all()
    
    return render_template("tasks.html", tasks=tasks, form=TaskForm())

@tasks_bp.route("/tasks/create", methods=["POST"])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        db = SessionLocal()
        task = Task(
        title = form.title.data,
        description = form.description.data,
        user_id = current_user.id
        )
        db.add(task)
        db.commit()
    else:
        flash("Error de datos en el formulario", "error")
    
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