"""
ETL para importação da tabela de empresas (dados cadastrais) a partir de CSV.

Arquivo sem cabeçalho (encoding Latin-1, separador ;, aspas duplas).
Formato: K3241.K03200Y0.D60110.EMPRECSV
  "cnpj_basico";"razao_social";"natureza_juridica";"qualificacao_responsavel";"capital_social";"porte_empresa";"ente_federativo"

O campo capital_social vem com vírgula como separador decimal (ex.: "0,00", "1000,00").
"""
from decimal import Decimal
from collections.abc import Sequence

from app.etl.base import BaseCSVPipeline
from app.models.empresa import Empresa
from app.repositories.empresa import EmpresaRepository


class EmpresasPipeline(BaseCSVPipeline):
    """Importa empresas a partir de CSV (EMPRECSV), sem linha de cabeçalho."""

    fieldnames = (
        "cnpj_basico",
        "razao_social",
        "natureza_juridica",
        "qualificacao_responsavel",
        "capital_social",
        "porte_empresa",
        "ente_federativo",
    )
    encoding = "latin-1"  # Arquivos Receita Federal
    expected_columns = set(fieldnames)

    def __init__(self, session):
        super().__init__(session)
        self._repo = EmpresaRepository(session)

    def _validate_header(self, fieldnames: Sequence[str]) -> None:
        missing = self.expected_columns - set(fieldnames or [])
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes no CSV: {missing}")

    def _parse_capital_social(self, raw: str) -> Decimal:
        """Converte valor com vírgula decimal (ex: '1000,00') para Decimal."""
        if not raw or not raw.strip():
            return Decimal("0.00")
        # Remove espaços e troca vírgula por ponto
        normalized = (raw.strip()).replace(",", ".")
        try:
            return Decimal(normalized)
        except Exception:
            return Decimal("0.00")

    def transform_row(self, row: dict[str, str]) -> Empresa | None:
        cnpj_basico = (row.get("cnpj_basico") or "").strip()
        razao_social = (row.get("razao_social") or "").strip()
        if not cnpj_basico or not razao_social:
            return None

        natureza_juridica = (row.get("natureza_juridica") or "").strip()
        qualificacao_responsavel = (row.get("qualificacao_responsavel") or "").strip()
        capital_social = self._parse_capital_social(row.get("capital_social") or "0,00")
        porte_empresa = (row.get("porte_empresa") or "").strip() or "00"
        ente_raw = (row.get("ente_federativo") or "").strip()
        ente_federativo = ente_raw if ente_raw else None

        return Empresa(
            cnpj_basico=cnpj_basico[:10],
            razao_social=razao_social,
            natureza_juridica=natureza_juridica[:7],
            qualificacao_responsavel=qualificacao_responsavel[:7],
            capital_social=capital_social,
            porte_empresa=porte_empresa[:2],
            ente_federativo=ente_federativo,
        )

    async def _persist_one(self, model: Empresa) -> str:
        """Insere ou atualiza uma empresa por cnpj_basico via repository."""
        existing = await self._repo.get_by_cnpj_basico(model.cnpj_basico)
        if existing is not None:
            if (
                existing.razao_social == model.razao_social
                and existing.natureza_juridica == model.natureza_juridica
                and existing.qualificacao_responsavel == model.qualificacao_responsavel
                and existing.capital_social == model.capital_social
                and existing.porte_empresa == model.porte_empresa
                and existing.ente_federativo == model.ente_federativo
            ):
                return "skipped"
            existing.razao_social = model.razao_social
            existing.natureza_juridica = model.natureza_juridica
            existing.qualificacao_responsavel = model.qualificacao_responsavel
            existing.capital_social = model.capital_social
            existing.porte_empresa = model.porte_empresa
            existing.ente_federativo = model.ente_federativo
            await self._repo.update(existing)
            return "updated"
        await self._repo.create(model)
        return "inserted"
