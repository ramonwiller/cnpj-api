from app.etl.pipelines.cnaes import CnaesPipeline
from app.etl.pipelines.empresas import EmpresasPipeline
from app.etl.pipelines.municipios import MunicipiosPipeline
from app.etl.pipelines.naturezas import NaturezasPipeline
from app.etl.pipelines.paises import PaisesPipeline
from app.etl.pipelines.qualificacoes import QualificacoesPipeline

__all__ = [
    "CnaesPipeline",
    "EmpresasPipeline",
    "MunicipiosPipeline",
    "NaturezasPipeline",
    "PaisesPipeline",
    "QualificacoesPipeline",
]
