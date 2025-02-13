from fastapi import FastAPI
from typing import Optional

app= FastAPI()

@app.get('/')
def index():
    return 'hey'



from pydantic import BaseModel  

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.get('/blog')
def index(limit=10,sort: Optional[str]=None): # default limit is 10
    return {'data': f'{limit} blogs from the db'} 

@app.post('/blog')
def create_blog(blog: Blog):  #def create_blog(request: Blog):
    return {'data': f'{blog.title} has been created'}  