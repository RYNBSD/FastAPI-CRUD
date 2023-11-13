from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .model import connectDB, createTables

createTables()
app = FastAPI()

@app.get("/blogs", status_code=status.HTTP_200_OK, tags=["blogs"])
def get_blogs():
  con = connectDB()
  cur = con.cursor(dictionary=True)

  try:
    cur.execute("SELECT * FROM blogs")
    blogs = jsonable_encoder(cur.fetchall())
    return JSONResponse({
      "success": True,
      "blogs": blogs
    }, status.HTTP_200_OK if len(blogs) > 0 else status.HTTP_204_NO_CONTENT)
  except Exception as e:
    return JSONResponse({
      "success":  False,
      "message": str(e)
    }, status.HTTP_500_INTERNAL_SERVER_ERROR)

class BlogBody(BaseModel):
  title: str
  description: str

@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def post_blogs(body: BlogBody):
  con = connectDB()
  cur = con.cursor()

  try:
    cur.execute("INSERT INTO blogs (title,  description) VALUES (%s, %s)", (body.title, body.description))
    con.commit()
    return JSONResponse({
      "success": True,
    }, status.HTTP_201_CREATED)
  except Exception as e:
    return JSONResponse({
      "success":  False,
      "message": str(e)
    }, status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.put("/blog/{id}", status_code=status.HTTP_200_OK, tags=["blogs"])
def put_blogs(id: int, body: BlogBody):
  con = connectDB()
  cur = con.cursor()

  try:
    cur.execute("UPDATE blogs SET title=%s,  description=%s WHERE id=%s", (body.title, body.description, id))
    con.commit()
    
    return JSONResponse({
      "success": True,
    }, status.HTTP_200_OK)
  except Exception as e:
    return JSONResponse({
      "success":  False,
      "message": str(e)
    }, status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.delete("/blog/{id}", status_code=status.HTTP_200_OK, tags=["blogs"])
def delete_blogs(id: int):
  con = connectDB()
  cur = con.cursor()

  try:
    cur.execute("DELETE FROM blogs  WHERE id=%s", (id,))
    con.commit()
    
    return JSONResponse({
      "success": True,
    }, status.HTTP_200_OK)
  except Exception as e:
    return JSONResponse({
      "success":  False,
      "message": str(e)
    }, status.HTTP_500_INTERNAL_SERVER_ERROR)
