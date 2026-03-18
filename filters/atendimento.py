from qdrant_client import models
import re

def monta_filtro_atendimento(query:str) -> list | None:
    atendimentos = re.findall(r'\b\d{9}\b', query)

    if not atendimentos:
        return None
    
    filtros = []
    
    if len(atendimentos) == 1:
        tipo = 'must'
    else:
        tipo = 'should'

    for atendimento in atendimentos:
        filtros.append({
            'tipo': tipo,
            'filtro': models.FieldCondition(key='atendimento_id', match=models.MatchValue(value=int(atendimento)))
        })

    return filtros