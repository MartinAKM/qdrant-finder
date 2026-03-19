from qdrant_client.http import models
from qdrant_client import QdrantClient
from services.embedder import cria_embeddings_query
from filters.gera_filtros import monta_filtros
import os

def normaliza_query(query:str) -> str:
    return query.upper()

def execute_search(client:QdrantClient, model, query:str):
    query = normaliza_query(query)

    embeds = cria_embeddings_query(model, query)

    filtros = monta_filtros(query)

    print('\n\n\nfiltros:', filtros, '\n\n\n')

    resultado_busca = client.query_points(
        collection_name=os.getenv('NOME_COLLECTION'),
        prefetch=[
            models.Prefetch(
                query=embeds[0],
                using='dense',
                limit=os.getenv('RETURN_POINTS_LIMIT')
            ),
            models.Prefetch(
                query=embeds[1],
                using='sparse',
                limit=os.getenv('RETURN_POINTS_LIMIT')
            )
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        query_filter=filtros,
        limit=os.getenv('RETURN_POINTS_LIMIT'),
        score_threshold=0.3
    )

    return resultado_busca.points