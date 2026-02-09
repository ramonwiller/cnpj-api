"""
ETL para importação da tabela Simples Nacional a partir de CSV.

Arquivo sem cabeçalho (encoding Latin-1, separador ;, aspas duplas).
Formato Receita Federal: K3241.K03200Y0.D60110.SIMPLES.CSV
Layout: cnpj_basico; opcao_simples; data_opcao_simples; data_exclusao_simples;
        opcao_mei; data_opcao_mei; data_exclusao_mei
Datas no formato YYYYMMDD.
"""
from datetime import date
from collections.abc import Sequence

from app.etl.base import BaseCSVPipeline
from app.models.simples import Simples, OpcaoSimples, OpcaoMei
from app.repositories.simples import SimplesRepository


def _parse_date(raw: str) -> date | None:
    """Converte YYYYMMDD para date; string vazia retorna None."""
    raw = (raw or "").strip()
    if not raw or len(raw) != 8:
        return None
    try:
        return date(int(raw[:4]), int(raw[4:6]), int(raw[6:8]))
    except (ValueError, TypeError):
        return None


def _normalize_opcao(raw: str) -> str:
    """Normaliza opção Simples/MEI: S, N ou vazio."""
    v = (raw or "").strip().upper()
    if v == "S":
        return "S"
    if v == "N":
        return "N"
    return ""


class SimplesPipeline(BaseCSVPipeline):
    """Importa Simples Nacional a partir de CSV (SIMPLES.CSV), sem linha de cabeçalho."""

    fieldnames = (
        "cnpj_basico",
        "opcao_simples",
        "data_opcao_simples",
        "data_exclusao_simples",
        "opcao_mei",
        "data_opcao_mei",
        "data_exclusao_mei",
    )
    encoding = "latin-1"
    expected_columns = set(fieldnames)

    def __init__(self, session):
        super().__init__(session)
        self._repo = SimplesRepository(session)

    def _validate_header(self, fieldnames: Sequence[str]) -> None:
        missing = self.expected_columns - set(fieldnames or [])
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes no CSV: {missing}")

    def transform_row(self, row: dict[str, str]) -> Simples | None:
        cnpj_basico = (row.get("cnpj_basico") or "").strip()[:10]
        if not cnpj_basico:
            return None

        opcao_simples = _normalize_opcao(row.get("opcao_simples") or "")
        data_opcao_simples = _parse_date(row.get("data_opcao_simples") or "")
        data_exclusao_simples = _parse_date(row.get("data_exclusao_simples") or "")
        opcao_mei = _normalize_opcao(row.get("opcao_mei") or "")
        data_opcao_mei = _parse_date(row.get("data_opcao_mei") or "")
        data_exclusao_mei = _parse_date(row.get("data_exclusao_mei") or "")

        return Simples(
            cnpj_basico=cnpj_basico,
            opcao_simples=opcao_simples or OpcaoSimples.OUTROS,
            data_opcao_simples=data_opcao_simples,
            data_exclusao_simples=data_exclusao_simples,
            opcao_mei=opcao_mei or OpcaoMei.OUTROS,
            data_opcao_mei=data_opcao_mei,
            data_exclusao_mei=data_exclusao_mei,
        )

    async def _persist_one(self, model: Simples) -> str:
        """Insere ou atualiza um registro de Simples por cnpj_basico."""
        existing = await self._repo.get_by_cnpj_basico(model.cnpj_basico)
        if existing is not None:
            if (
                existing.opcao_simples == model.opcao_simples
                and existing.data_opcao_simples == model.data_opcao_simples
                and existing.data_exclusao_simples == model.data_exclusao_simples
                and existing.opcao_mei == model.opcao_mei
                and existing.data_opcao_mei == model.data_opcao_mei
                and existing.data_exclusao_mei == model.data_exclusao_mei
            ):
                return "skipped"
            existing.opcao_simples = model.opcao_simples
            existing.data_opcao_simples = model.data_opcao_simples
            existing.data_exclusao_simples = model.data_exclusao_simples
            existing.opcao_mei = model.opcao_mei
            existing.data_opcao_mei = model.data_opcao_mei
            existing.data_exclusao_mei = model.data_exclusao_mei
            await self._repo.update(existing)
            return "updated"
        await self._repo.create(model)
        return "inserted"
