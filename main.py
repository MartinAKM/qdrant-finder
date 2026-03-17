from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from model.request import Request
from services.qdrant import execute_search
import os

load_dotenv()

print('Iniciando model...')
model = SentenceTransformer(os.getenv('MODEL_EMBEDDER'))
print('Concluído')

print('Iniciando conexão com qdrant...')
client = QdrantClient(os.getenv('URL_QDRANT'))
print('Concluído')

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def test():
    return { 'text': 'API up and running!' }


@app.post('/find')
def response(request:Request):
    documentos = execute_search(client, model, request.query)
    return documentos