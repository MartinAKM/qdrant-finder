from sentence_transformers import SentenceTransformer
from qdrant_client.http import models

def retorna_embedd_esparso(model:SentenceTransformer, query:str):
    pesos_lexicos = model.encode(query, return_components=True)['lexical_weights']
    
    indices = [int(k) for k in pesos_lexicos.keys()]
    valores = [float(v) for v in pesos_lexicos.values()]

    return models.SparseVector(indices, valores)

def cria_embeddings_query(model:SentenceTransformer, query:str) -> tuple:
    embedd_denso = model.encode(query).tolist()
    embedd_esparso = retorna_embedd_esparso(model, query)

    return (embedd_denso, embedd_esparso)