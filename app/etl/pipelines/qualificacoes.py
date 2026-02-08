"""
ETL para importação da tabela de qualificações (sócios) a partir de CSV.

Arquivo sem cabeçalho (encoding Latin-1, separador ;, aspas duplas):
  "0001";"SÓCIO ADMINISTRADOR"
  "0002";"SÓCIO COM CAPITAL SOCIAL"
  "0490";"ADMINISTRADOR"
"""
from collections.abc import Sequence

from app.etl.base import BaseCSVPipeline
from app.models.qualificacao import Qualificacao
from app.repositories.qualificacao import QualificacaoRepository


class QualificacoesPipeline(BaseCSVPipeline):
    """Importa qualificações a partir de CSV (codigo;descricao), sem linha de cabeçalho."""

    fieldnames = ("codigo", "descricao")
    encoding = "latin-1"  # Arquivos Receita Federal (ex.: acentos em "SÓCIO")
    expected_columns = {"codigo", "descricao"}

    def __init__(self, session):
        super().__init__(session)
        self._repo = QualificacaoRepository(session)

    def _validate_header(self, fieldnames: Sequence[str]) -> None:
        missing = self.expected_columns - set(fieldnames or [])
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes no CSV: {missing}")

    def transform_row(self, row: dict[str, str]) -> Qualificacao | None:
        codigo = (row.get("codigo") or "").strip()
        descricao = (row.get("descricao") or "").strip()
        if not codigo or not descricao:
            return None
        return Qualificacao(codigo=codigo[:7], descricao=descricao)

    async def _persist_one(self, model: Qualificacao) -> str:
        """Insere ou atualiza uma qualificação por código via repository; ignora se já estiver igual (skipped)."""
        existing = await self._repo.get_by_codigo(model.codigo)
        if existing is not None:
            if existing.descricao == model.descricao:
                return "skipped"
            existing.descricao = model.descricao
            await self._repo.update(existing)
            return "updated"
        await self._repo.create(model)
        return "inserted"
