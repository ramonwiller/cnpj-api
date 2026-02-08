"""
ETL para importação da tabela de CNAEs (atividades econômicas) a partir de CSV.

Arquivo sem cabeçalho (encoding Latin-1, separador ;, aspas duplas):
  "01113";"Cultivo de cereais"
  "4712101";"Comércio varejista de mercadorias em geral"
  "6201501";"Desenvolvimento de programas de computador sob encomenda"
"""
from collections.abc import Sequence

from app.etl.base import BaseCSVPipeline
from app.models.cnae import Cnae
from app.repositories.cnae import CnaeRepository


class CnaesPipeline(BaseCSVPipeline):
    """Importa CNAEs a partir de CSV (codigo;descricao), sem linha de cabeçalho."""

    fieldnames = ("codigo", "descricao")
    encoding = "latin-1"  # Arquivos Receita Federal (ex.: acentos em descrições)
    expected_columns = {"codigo", "descricao"}

    def __init__(self, session):
        super().__init__(session)
        self._repo = CnaeRepository(session)

    def _validate_header(self, fieldnames: Sequence[str]) -> None:
        missing = self.expected_columns - set(fieldnames or [])
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes no CSV: {missing}")

    def transform_row(self, row: dict[str, str]) -> Cnae | None:
        codigo = (row.get("codigo") or "").strip()
        descricao = (row.get("descricao") or "").strip()
        if not codigo or not descricao:
            return None
        return Cnae(codigo=codigo[:7], descricao=descricao)

    async def _persist_one(self, model: Cnae) -> str:
        """Insere ou atualiza um CNAE por código via repository; ignora se já estiver igual (skipped)."""
        existing = await self._repo.get_by_codigo(model.codigo)
        if existing is not None:
            if existing.descricao == model.descricao:
                return "skipped"
            existing.descricao = model.descricao
            await self._repo.update(existing)
            return "updated"
        await self._repo.create(model)
        return "inserted"
