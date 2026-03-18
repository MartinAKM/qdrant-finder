from qdrant_client import models
from filters.atendimento import monta_filtro_atendimento

def monta_filtros(query:str) -> models.Filter | None:
    filtros = []

    filtros.append(monta_filtro_atendimento(query))

    filtros_qdrant = {
        'must': [],
        'must_not': [],
        'should': []
    }

    for filtro in filtros:
        if not filtro:
            continue
        
        for condicao in filtro:
            filtros_qdrant[condicao['tipo']].append(condicao['filtro'])
    
    if not (filtros_qdrant['must'] or
            filtros_qdrant['must_not'] or
            filtros_qdrant['should']):
        return None

    return models.Filter(
        must=filtros_qdrant['must'],
        must_not=filtros_qdrant['must_not'],
        should=filtros_qdrant['should']
    )