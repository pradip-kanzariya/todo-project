from fastapi import FastAPI, Depends, HTTPException
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from models import Todo
from schemas import CreateTodo

app = FastAPI()
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all todos.
@app.get("/todo")
def todo_home(db: Session=Depends(get_db)):
    try:
        all_todos = db.query(Todo).all()
        return all_todos
    except Exception as e:
        print((f"Error : {e}"))

# Create new todo.
@app.post("/todo/create")
def todo_create(todo: CreateTodo, db: Session=Depends(get_db)):
    new_todo = Todo(
        title = todo.title,
        description = todo.description
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# Edit todo.
@app.patch("/todo/edit/{todo_id}")
def todo_edit(todo_id: int, todo: CreateTodo, db: Session=Depends(get_db)):
    get_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not get_todo:
        raise HTTPException(status_code=404, detail="No data.")
    
    get_todo.title = todo.title
    get_todo.description = todo.description
    db.commit()
    db.refresh(get_todo)
    
    return {"message": "Todo Updated successfully."}

# Delete todo.
@app.delete("/todo/delete/{todo_id}")
def todo_delete(todo_id: int, db: Session=Depends(get_db)):
    get_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not get_todo:
        raise HTTPException(status_code=404, detail="No data.")
    
    db.delete(get_todo)
    db.commit()
    return {"message": "Todo Deleted successfully."}
