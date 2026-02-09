"""
ETL para importação da tabela de estabelecimentos a partir de CSV.

Arquivo sem cabeçalho (encoding Latin-1, separador ;, aspas duplas).
Formato: K3241.K03200Y0.D60110.ESTABELE
Layout Receita Federal: cnpj_basico; cnpj_ordem; cnpj_dv; identificador_matriz_filial;
nome_fantasia; situacao_cadastral; data_situacao_cadastral; motivo_situacao_cadastral;
nome_cidade_exterior; pais; data_inicio_atividade; cnae_fiscal_principal; cnae_fiscal_secundaria;
tipo_logradouro; logradouro; numero; complemento; bairro; cep; uf; municipio;
ddd1; telefone1; ddd2; telefone2; ddd_fax; fax; correio_eletronico; situacao_especial; data_situacao_especial
"""
from datetime import date
from collections.abc import Sequence

from app.etl.base import BaseCSVPipeline
from app.models.estabelecimento import Estabelecimento
from app.repositories.estabelecimento import EstabelecimentoRepository


def _parse_date(raw: str) -> date | None:
    """Converte YYYYMMDD para date; string vazia retorna None."""
    raw = (raw or "").strip()
    if not raw or len(raw) != 8:
        return None
    try:
        return date(int(raw[:4]), int(raw[4:6]), int(raw[6:8]))
    except (ValueError, TypeError):
        return None


def _str_or_none(raw: str, max_len: int | None = None) -> str | None:
    s = (raw or "").strip()
    if not s:
        return None
    return s[:max_len] if max_len else s


class EstabelecimentosPipeline(BaseCSVPipeline):
    """Importa estabelecimentos a partir de CSV (ESTABELE), sem linha de cabeçalho."""

    fieldnames = (
        "cnpj_basico",
        "cnpj_ordem",
        "cnpj_dv",
        "identificador_matriz_filial",
        "nome_fantasia",
        "situacao_cadastral",
        "data_situacao_cadastral",
        "motivo_situacao_cadastral",
        "nome_cidade_exterior",
        "pais",
        "data_inicio_atividade",
        "cnae_fiscal_principal",
        "cnae_fiscal_secundaria",
        "tipo_logradouro",
        "logradouro",
        "numero",
        "complemento",
        "bairro",
        "cep",
        "uf",
        "municipio",
        "ddd1",
        "telefone1",
        "ddd2",
        "telefone2",
        "ddd_fax",
        "fax",
        "correio_eletronico",
        "situacao_especial",
        "data_situacao_especial",
    )
    encoding = "latin-1"
    expected_columns = set(fieldnames)

    def __init__(self, session):
        super().__init__(session)
        self._repo = EstabelecimentoRepository(session)

    def _validate_header(self, fieldnames: Sequence[str]) -> None:
        missing = self.expected_columns - set(fieldnames or [])
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes no CSV: {missing}")

    def transform_row(self, row: dict[str, str]) -> Estabelecimento | None:
        cnpj_basico = (row.get("cnpj_basico") or "").strip()[:10]
        cnpj_ordem = (row.get("cnpj_ordem") or "").strip()[:4]
        cnpj_dv = (row.get("cnpj_dv") or "").strip()[:2]
        if not cnpj_basico or not cnpj_ordem or not cnpj_dv:
            return None

        data_situacao_cadastral = _parse_date(row.get("data_situacao_cadastral") or "")
        if data_situacao_cadastral is None:
            return None

        identificador_matriz_filial = (row.get("identificador_matriz_filial") or "1").strip()[:1] or "1"
        nome_fantasia = (row.get("nome_fantasia") or "").strip() or ""
        situacao_cadastral = (row.get("situacao_cadastral") or "01").strip()[:2] or "01"
        motivo_situacao_cadastral = (row.get("motivo_situacao_cadastral") or "").strip()[:7]
        if not motivo_situacao_cadastral:
            return None

        nome_cidade_exterior = _str_or_none(row.get("nome_cidade_exterior"))
        pais = _str_or_none(row.get("pais"), 7)
        data_inicio_atividade = _parse_date(row.get("data_inicio_atividade") or "")
        cnae_fiscal_principal = (row.get("cnae_fiscal_principal") or "").strip()[:7]
        if not cnae_fiscal_principal:
            return None
        cnae_fiscal_secundaria = _str_or_none(row.get("cnae_fiscal_secundaria"))
        tipo_logradouro = (row.get("tipo_logradouro") or "").strip() or ""
        logradouro = (row.get("logradouro") or "").strip() or ""
        numero = (row.get("numero") or "").strip() or ""
        complemento = _str_or_none(row.get("complemento"))
        bairro = (row.get("bairro") or "").strip() or ""
        cep = (row.get("cep") or "").strip().replace("-", "")[:8] or ""
        uf = (row.get("uf") or "").strip()[:2] or ""
        municipio = (row.get("municipio") or "").strip()[:7] or ""
        if not tipo_logradouro or not logradouro or not numero or not bairro or not cep or not uf or not municipio:
            return None

        ddd1 = _str_or_none(row.get("ddd1"), 2)
        telefone1 = _str_or_none(row.get("telefone1"))
        ddd2 = _str_or_none(row.get("ddd2"), 2)
        telefone2 = _str_or_none(row.get("telefone2"))
        ddd_fax = _str_or_none(row.get("ddd_fax"), 2)
        fax = _str_or_none(row.get("fax"))
        correio_eletronico = _str_or_none(row.get("correio_eletronico"))
        situacao_especial = _str_or_none(row.get("situacao_especial"))
        data_situacao_especial = _parse_date(row.get("data_situacao_especial") or "")

        return Estabelecimento(
            cnpj_basico=cnpj_basico,
            cnpj_ordem=cnpj_ordem,
            cnpj_dv=cnpj_dv,
            identificador_matriz_filial=identificador_matriz_filial,
            nome_fantasia=nome_fantasia,
            situacao_cadastral=situacao_cadastral,
            data_situacao_cadastral=data_situacao_cadastral,
            motivo_situacao_cadastral=motivo_situacao_cadastral,
            nome_cidade_exterior=nome_cidade_exterior,
            pais=pais,
            data_inicio_atividade=data_inicio_atividade,
            cnae_fiscal_principal=cnae_fiscal_principal,
            cnae_fiscal_secundaria=cnae_fiscal_secundaria,
            tipo_logradouro=tipo_logradouro,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cep=cep,
            uf=uf,
            municipio=municipio,
            ddd1=ddd1,
            telefone1=telefone1,
            ddd2=ddd2,
            telefone2=telefone2,
            ddd_fax=ddd_fax,
            fax=fax,
            correio_eletronico=correio_eletronico,
            situacao_especial=situacao_especial,
            data_situacao_especial=data_situacao_especial,
        )

    async def _persist_one(self, model: Estabelecimento) -> str:
        existing = await self._repo.get_by_cnpj(
            model.cnpj_basico, model.cnpj_ordem, model.cnpj_dv
        )
        if existing is not None:
            # Comparação simplificada: se todos os campos relevantes iguais, skip
            if (
                existing.nome_fantasia == model.nome_fantasia
                and existing.situacao_cadastral == model.situacao_cadastral
                and existing.data_situacao_cadastral == model.data_situacao_cadastral
                and existing.motivo_situacao_cadastral == model.motivo_situacao_cadastral
                and existing.cnae_fiscal_principal == model.cnae_fiscal_principal
                and existing.logradouro == model.logradouro
                and existing.numero == model.numero
                and existing.cep == model.cep
                and existing.uf == model.uf
                and existing.municipio == model.municipio
            ):
                return "skipped"
            existing.identificador_matriz_filial = model.identificador_matriz_filial
            existing.nome_fantasia = model.nome_fantasia
            existing.situacao_cadastral = model.situacao_cadastral
            existing.data_situacao_cadastral = model.data_situacao_cadastral
            existing.motivo_situacao_cadastral = model.motivo_situacao_cadastral
            existing.nome_cidade_exterior = model.nome_cidade_exterior
            existing.pais = model.pais
            existing.data_inicio_atividade = model.data_inicio_atividade
            existing.cnae_fiscal_principal = model.cnae_fiscal_principal
            existing.cnae_fiscal_secundaria = model.cnae_fiscal_secundaria
            existing.tipo_logradouro = model.tipo_logradouro
            existing.logradouro = model.logradouro
            existing.numero = model.numero
            existing.complemento = model.complemento
            existing.bairro = model.bairro
            existing.cep = model.cep
            existing.uf = model.uf
            existing.municipio = model.municipio
            existing.ddd1 = model.ddd1
            existing.telefone1 = model.telefone1
            existing.ddd2 = model.ddd2
            existing.telefone2 = model.telefone2
            existing.ddd_fax = model.ddd_fax
            existing.fax = model.fax
            existing.correio_eletronico = model.correio_eletronico
            existing.situacao_especial = model.situacao_especial
            existing.data_situacao_especial = model.data_situacao_especial
            await self._repo.update(existing)
            return "updated"
        await self._repo.create(model)
        return "inserted"
