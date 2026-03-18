from qdrant_client.http import models

def retorna_embedd_esparso(encode):
    pesos_lexicos = encode['lexical_weights']
    
    indices = [int(k) for k in pesos_lexicos.keys()]
    valores = [float(v) for v in pesos_lexicos.values()]

    return models.SparseVector(indices, valores)

def cria_embeddings_query(model, query:str) -> tuple:
    encode = model.encode(query, return_dense=True, return_sparse=True, return_colbert_vecs=False)

    embedd_denso = encode['dense_vecs'].tolist()
    embedd_esparso = None#retorna_embedd_esparso(encode)

    return (embedd_denso, embedd_esparso)