from app.etl.pipelines.cnaes import CnaesPipeline
from app.etl.pipelines.municipios import MunicipiosPipeline
from app.etl.pipelines.naturezas import NaturezasPipeline
from app.etl.pipelines.paises import PaisesPipeline
from app.etl.pipelines.qualificacoes import QualificacoesPipeline

__all__ = [
    "CnaesPipeline",
    "MunicipiosPipeline",
    "NaturezasPipeline",
    "PaisesPipeline",
    "QualificacoesPipeline",
]
