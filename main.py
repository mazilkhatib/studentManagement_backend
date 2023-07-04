from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="student_management"
    )

@app.get("/students")
def get_students():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        students = [
            {"id": row[0], "name": row[1], "age": row[2]}
            for row in cursor.fetchall()
        ]
        return students
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

@app.post("/students")
def create_student(student: dict):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        query = "INSERT INTO students (name, age) VALUES (%s, %s)"
        values = (student["name"], student["age"])
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Student created successfully"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

@app.put("/students/{student_id}")
def update_student(student_id: int, student: dict):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        query = "UPDATE students SET name = %s, age = %s WHERE id = %s"
        values = (student["name"], student["age"], student_id)
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Student updated successfully"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        query = "DELETE FROM students WHERE id = %s"
        values = (student_id,)
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Student deleted successfully"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
