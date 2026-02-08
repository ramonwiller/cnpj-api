import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Raiz do projeto (para resolver caminhos relativos)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# Garante que o projeto está no path (rodar de qualquer diretório)
sys.path.insert(0, str(PROJECT_ROOT))

from app.etl.session import get_async_session
from app.etl.pipelines import (
    CnaesPipeline,
    MunicipiosPipeline,
    NaturezasPipeline,
    PaisesPipeline,
    QualificacoesPipeline,
)


def _resolve_path(file_path: str) -> Path:
    """Resolve caminho: se for relativo, usa a raiz do projeto como base."""
    p = Path(file_path)
    return (PROJECT_ROOT / p) if not p.is_absolute() else p


def _setup_logging(quiet: bool, debug: bool = False) -> None:
    if debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s [%(name)s] %(message)s",
            stream=sys.stderr,
        )
        logging.getLogger("app.etl").setLevel(logging.DEBUG)
    elif quiet:
        logging.getLogger("app.etl").setLevel(logging.WARNING)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            stream=sys.stderr,
        )


async def _cmd_paises(args: argparse.Namespace) -> int:
    path = _resolve_path(args.file)
    if not path.exists():
        print(f"Erro: arquivo não encontrado: {path}", file=sys.stderr)
        return 1
    quiet = getattr(args, "quiet", False)
    debug = getattr(args, "debug", False)
    _setup_logging(quiet, debug)
    async with get_async_session() as session:
        pipeline = PaisesPipeline(session)
        if getattr(args, "dry_run", False):
            # Dry-run: só valida header e primeira linha
            with path.open(newline="", encoding=pipeline.encoding) as f:
                import csv
                r = csv.DictReader(
                    f,
                    delimiter=pipeline.delimiter,
                    fieldnames=list(pipeline.fieldnames) if pipeline.fieldnames else None,
                )
                pipeline._validate_header(list(r.fieldnames or []))
                for i, row in enumerate(r):
                    if i >= 1:
                        break
                    pipeline.transform_row(row)
            print("Dry-run OK: CSV válido.")
            return 0
        stats = await pipeline.run(path, show_progress=not quiet, debug=debug)
    print("ETL concluído:", stats)
    return 0


async def _cmd_municipios(args: argparse.Namespace) -> int:
    path = _resolve_path(args.file)
    if not path.exists():
        print(f"Erro: arquivo não encontrado: {path}", file=sys.stderr)
        return 1
    quiet = getattr(args, "quiet", False)
    debug = getattr(args, "debug", False)
    _setup_logging(quiet, debug)
    async with get_async_session() as session:
        pipeline = MunicipiosPipeline(session)
        if getattr(args, "dry_run", False):
            with path.open(newline="", encoding=pipeline.encoding) as f:
                import csv
                r = csv.DictReader(
                    f,
                    delimiter=pipeline.delimiter,
                    fieldnames=list(pipeline.fieldnames) if pipeline.fieldnames else None,
                )
                pipeline._validate_header(list(r.fieldnames or []))
                for i, row in enumerate(r):
                    if i >= 1:
                        break
                    pipeline.transform_row(row)
            print("Dry-run OK: CSV válido.")
            return 0
        stats = await pipeline.run(path, show_progress=not quiet, debug=debug)
    print("ETL concluído:", stats)
    return 0


async def _cmd_qualificacoes(args: argparse.Namespace) -> int:
    path = _resolve_path(args.file)
    if not path.exists():
        print(f"Erro: arquivo não encontrado: {path}", file=sys.stderr)
        return 1
    quiet = getattr(args, "quiet", False)
    debug = getattr(args, "debug", False)
    _setup_logging(quiet, debug)
    async with get_async_session() as session:
        pipeline = QualificacoesPipeline(session)
        if getattr(args, "dry_run", False):
            with path.open(newline="", encoding=pipeline.encoding) as f:
                import csv
                r = csv.DictReader(
                    f,
                    delimiter=pipeline.delimiter,
                    fieldnames=list(pipeline.fieldnames) if pipeline.fieldnames else None,
                )
                pipeline._validate_header(list(r.fieldnames or []))
                for i, row in enumerate(r):
                    if i >= 1:
                        break
                    pipeline.transform_row(row)
            print("Dry-run OK: CSV válido.")
            return 0
        stats = await pipeline.run(path, show_progress=not quiet, debug=debug)
    print("ETL concluído:", stats)
    return 0


async def _cmd_naturezas(args: argparse.Namespace) -> int:
    path = _resolve_path(args.file)
    if not path.exists():
        print(f"Erro: arquivo não encontrado: {path}", file=sys.stderr)
        return 1
    quiet = getattr(args, "quiet", False)
    debug = getattr(args, "debug", False)
    _setup_logging(quiet, debug)
    async with get_async_session() as session:
        pipeline = NaturezasPipeline(session)
        if getattr(args, "dry_run", False):
            with path.open(newline="", encoding=pipeline.encoding) as f:
                import csv
                r = csv.DictReader(
                    f,
                    delimiter=pipeline.delimiter,
                    fieldnames=list(pipeline.fieldnames) if pipeline.fieldnames else None,
                )
                pipeline._validate_header(list(r.fieldnames or []))
                for i, row in enumerate(r):
                    if i >= 1:
                        break
                    pipeline.transform_row(row)
            print("Dry-run OK: CSV válido.")
            return 0
        stats = await pipeline.run(path, show_progress=not quiet, debug=debug)
    print("ETL concluído:", stats)
    return 0


async def _cmd_cnaes(args: argparse.Namespace) -> int:
    path = _resolve_path(args.file)
    if not path.exists():
        print(f"Erro: arquivo não encontrado: {path}", file=sys.stderr)
        return 1
    quiet = getattr(args, "quiet", False)
    debug = getattr(args, "debug", False)
    _setup_logging(quiet, debug)
    async with get_async_session() as session:
        pipeline = CnaesPipeline(session)
        if getattr(args, "dry_run", False):
            with path.open(newline="", encoding=pipeline.encoding) as f:
                import csv
                r = csv.DictReader(
                    f,
                    delimiter=pipeline.delimiter,
                    fieldnames=list(pipeline.fieldnames) if pipeline.fieldnames else None,
                )
                pipeline._validate_header(list(r.fieldnames or []))
                for i, row in enumerate(r):
                    if i >= 1:
                        break
                    pipeline.transform_row(row)
            print("Dry-run OK: CSV válido.")
            return 0
        stats = await pipeline.run(path, show_progress=not quiet, debug=debug)
    print("ETL concluído:", stats)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ETL CNPJ API")
    sub = parser.add_subparsers(dest="pipeline", required=True)

    p_paises = sub.add_parser("paises", help="Importar CSV de países")
    p_paises.add_argument(
        "file",
        help="Caminho do CSV (ex.: storage/F.K03200$Z.D60110.PAISCSV). Relativo à raiz do projeto ou absoluto.",
    )
    p_paises.add_argument("--dry-run", action="store_true", help="Apenas validar CSV")
    p_paises.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Sem barra de progresso nem logging",
    )
    p_paises.add_argument(
        "--debug",
        action="store_true",
        help="Exibir erros (traceback) e detalhes de cada operação (inserted/updated/skipped)",
    )
    p_paises.set_defaults(func=_cmd_paises)

    p_municipios = sub.add_parser("municipios", help="Importar CSV de municípios")
    p_municipios.add_argument(
        "file",
        help="Caminho do CSV (ex.: storage/F.K03200$Z.D60110.MUNICCSV). Relativo à raiz do projeto ou absoluto.",
    )
    p_municipios.add_argument("--dry-run", action="store_true", help="Apenas validar CSV")
    p_municipios.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Sem barra de progresso nem logging",
    )
    p_municipios.add_argument(
        "--debug",
        action="store_true",
        help="Exibir erros (traceback) e detalhes de cada operação (inserted/updated/skipped)",
    )
    p_municipios.set_defaults(func=_cmd_municipios)

    p_qualificacoes = sub.add_parser("qualificacoes", help="Importar CSV de qualificações (sócios)")
    p_qualificacoes.add_argument(
        "file",
        help="Caminho do CSV (ex.: storage/F.K03200$Z.D60110.QUALSCSV). Relativo à raiz do projeto ou absoluto.",
    )
    p_qualificacoes.add_argument("--dry-run", action="store_true", help="Apenas validar CSV")
    p_qualificacoes.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Sem barra de progresso nem logging",
    )
    p_qualificacoes.add_argument(
        "--debug",
        action="store_true",
        help="Exibir erros (traceback) e detalhes de cada operação (inserted/updated/skipped)",
    )
    p_qualificacoes.set_defaults(func=_cmd_qualificacoes)

    p_naturezas = sub.add_parser("naturezas", help="Importar CSV de naturezas jurídicas")
    p_naturezas.add_argument(
        "file",
        help="Caminho do CSV (ex.: storage/F.K03200$Z.D60110.NATJUCSV). Relativo à raiz do projeto ou absoluto.",
    )
    p_naturezas.add_argument("--dry-run", action="store_true", help="Apenas validar CSV")
    p_naturezas.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Sem barra de progresso nem logging",
    )
    p_naturezas.add_argument(
        "--debug",
        action="store_true",
        help="Exibir erros (traceback) e detalhes de cada operação (inserted/updated/skipped)",
    )
    p_naturezas.set_defaults(func=_cmd_naturezas)

    p_cnaes = sub.add_parser("cnaes", help="Importar CSV de CNAEs (atividades econômicas)")
    p_cnaes.add_argument(
        "file",
        help="Caminho do CSV (ex.: storage/F.K03200$Z.D60110.CNAECSV). Relativo à raiz do projeto ou absoluto.",
    )
    p_cnaes.add_argument("--dry-run", action="store_true", help="Apenas validar CSV")
    p_cnaes.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Sem barra de progresso nem logging",
    )
    p_cnaes.add_argument(
        "--debug",
        action="store_true",
        help="Exibir erros (traceback) e detalhes de cada operação (inserted/updated/skipped)",
    )
    p_cnaes.set_defaults(func=_cmd_cnaes)

    args = parser.parse_args()
    return asyncio.run(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
