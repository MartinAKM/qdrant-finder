from qdrant_client.http import models
from services.embedder import cria_embeddings_query
import os

def execute_search(client, model, query:str):
    embeds = cria_embeddings_query(model, query)

    filtros = None

    resultado_busca = client.query_points(
        collection_name=os.getenv('NOME_COLLECTION'),
        prefetch=[
            models.Prefetch(
                query=embeds[0],
                using='dense',
                limit=os.getenv('RETURN_POINTS_LIMIT')
            ),
            # models.Prefetch(
            #     query=embeds[1],
            #     using='sparse',
            #     limit=os.getenv('RETURN_POINTS_LIMIT')
            # )
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        query_filter=filtros,
        limit=os.getenv('RETURN_POINTS_LIMIT')
    )

    return resultado_busca.points