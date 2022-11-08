from sqlite3 import connect
from typing import Optional
from fastapi import  FastAPI,Response,status,HTTPException
from pydantic import BaseModel
import psycopg2
from time import sleep
from psycopg2.extras import RealDictCursor

posts_collection=[
    {"title":"deafult 1 title",
    "content":"deafult 1 content",
    "published" :True,
    "rating":None,
    "id":1},
    {"title":"deafult 2 title",
    "content":"deafult 2 content",
    "published" :False,
    "likes":0,
    "id":2}
    ]


app = FastAPI()

# title:str,content:str
class Post(BaseModel):
    title:str  # must
    content:str
    published:bool =True  # optional
    likes: Optional[int] = 0




while(True):
    try:
        connection=psycopg2.connect(host='localhost',database='fastapi_tutorial_db',
        user='postgres',password='postgresql',cursor_factory=RealDictCursor)
        cursor=connection.cursor()
        print("database connection is sucessfull")
        break
    except psycopg2.OperationalError as e:
        print('connection failed \n Error : ',e)
        sleep(2)


# if two function has same http method and path
#  function at first will be called

@app.get("/posts")
def get_post():
    cursor.execute("SELECT * FROM posts")
    posts=cursor.fetchall()
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict=post.dict()
    cursor.execute("""INSERT INTO posts (title,content,published,likes) 
    VALUES (%s,%s,%s,%s) RETURNING *""",tuple(post_dict.values()))
    new_post=cursor.fetchone()
    connection.commit()
    return {"data":new_post}


@app.get("/posts/{id}")
def get_post(id:int):  # fastapi automatically converts id to int bs given :int
    post=None
    cursor.execute("SELECT * FROM posts WHERE id= %s ",(str(id),))
    post=cursor.fetchone()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id = {id} doesnot exit")

    return {"data":post}
    
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("DELETE FROM posts WHERE id= %s RETURNING * ",(str(id),))
    if not cursor.fetchone():
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id = {id} doesnot exit")
    # when http 204 is used no data can be sent 
    connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post_put(id:int,changed_post:Post):
    post=None
    cursor.execute("UPDATE posts SET title=%s,content=%s,published=%s,likes=%s WHERE id= %s RETURNING *"
    ,(*changed_post.dict().values(),str(id),))
    post=cursor.fetchone()
    connection.commit()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id = {id} doesnot exit")

    return {"message":"sucessfully updated","data":post}
