"""
Base para pipelines ETL: leitura de CSV, validação e carga em lote.

Cada entidade (paises, cnae, etc.) pode ter um pipeline que:
- Define o caminho/stream do CSV e o schema de validação
- Usa transform_row e _persist_one (via repository) para mapear CSV -> modelos
- Herda batch_size para controle de memória
"""
import csv
import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from tqdm import tqdm

logger = logging.getLogger(__name__)


class BaseCSVPipeline(ABC):
    """Pipeline ETL genérico para importação de CSV."""

    # Ajuste conforme tamanho da memória e das linhas
    batch_size: int = 5_000

    # Se definido, o CSV não tem cabeçalho e essas serão os nomes das colunas (por ordem)
    fieldnames: Sequence[str] | None = None

    # Encoding do arquivo (arquivos da Receita Federal costumam ser Latin-1)
    encoding: str = "utf-8-sig"

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def run(
        self,
        path: Path | str,
        *,
        show_progress: bool = True,
        debug: bool = False,
    ) -> dict[str, int]:
        """
        Executa ETL: extrai do CSV, transforma e persiste um registro por vez (insert/update).
        Retorna estatísticas (processed, inserted, updated, errors).
        Se show_progress=True, exibe barra de progresso.
        Se debug=True, exibe erros (traceback) e detalhes de cada operação (inserted/updated/skipped).
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        stats: dict[str, int] = {"processed": 0, "inserted": 0, "updated": 0, "skipped": 0, "errors": 0}
        line_num = 0

        with path.open(newline="", encoding=self.encoding) as f:
            reader = csv.DictReader(
                f,
                delimiter=self.delimiter,
                fieldnames=list(self.fieldnames) if self.fieldnames else None,
            )
            self._validate_header(reader.fieldnames or [])

            rows = iter(reader)
            if show_progress:
                total = self._count_lines(path)
                rows = tqdm(
                    rows,
                    total=total,
                    unit=" linhas",
                    unit_scale=False,
                    desc="ETL",
                    leave=True,
                )

            for row in rows:
                line_num += 1
                try:
                    model = self.transform_row(row)
                    if model is not None:
                        result = await self._persist_one(model)
                        stats["processed"] += 1
                        if result == "inserted":
                            stats["inserted"] += 1
                        elif result == "updated":
                            stats["updated"] += 1
                        elif result == "skipped":
                            stats["skipped"] += 1
                        if debug:
                            codigo = getattr(model, "codigo", None)
                            logger.debug(
                                "linha %d: %s codigo=%s descricao=%s",
                                line_num,
                                result,
                                codigo,
                                getattr(model, "descricao", "")[:50],
                            )
                except Exception:
                    stats["errors"] += 1
                    if debug:
                        logger.exception("linha %d: erro ao processar row=%s", line_num, row)
                    self.on_row_error(row)
                    # Rollback para que a próxima linha rode em transação limpa (evita InFailedSqlTransaction)
                    await self.session.rollback()

        return stats

    def _count_lines(self, path: Path) -> int | None:
        """Conta linhas do arquivo para a barra de progresso (opcional)."""
        try:
            with path.open(newline="", encoding=self.encoding) as f:
                return sum(1 for _ in f)
        except OSError:
            return None

    @property
    def delimiter(self) -> str:
        return ";"

    def _validate_header(self, fieldnames: Sequence[str]) -> None:
        """Override para validar colunas esperadas do CSV."""
        pass

    @abstractmethod
    def transform_row(self, row: dict[str, str]) -> Any | None:
        """Converte uma linha do CSV no modelo SQLAlchemy (ou None para pular)."""
        ...

    @abstractmethod
    async def _persist_one(self, model: Any) -> str:
        """
        Persiste um único registro via repository (insert ou update).
        Retorna 'inserted', 'updated' ou 'skipped'.
        Implementado em cada pipeline usando o repository da entidade.
        """
        ...

    def on_row_error(self, row: dict[str, str]) -> None:
        """Callback opcional quando uma linha falha na transformação."""
        pass
