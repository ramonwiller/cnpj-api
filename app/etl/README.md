# ETL no projeto FastAPI

Rotinas de **Extract, Transform, Load** para importar CSVs (e outros arquivos) para o banco de dados, mantidas dentro do próprio projeto para reutilizar modelos, config e conexão.

## Organização recomendada

```
app/etl/
├── __init__.py
├── README.md           # este arquivo
├── session.py          # Sessão SQLAlchemy síncrona (ETL em lote)
├── base.py             # BaseCSVPipeline: leitura em lote, validação, stats
├── __main__.py         # CLI: python -m app.etl <pipeline> <arquivo>
└── pipelines/          # Um módulo por entidade ou fonte de dados
    ├── __init__.py
    ├── paises.py       # PaisesPipeline
    ├── cnae.py         # (exemplo futuro)
    └── ...
```

### Por que sessão síncrona?

- A API usa `asyncpg` (async) para baixa latência.
- ETL faz **carga em lote** (muitas linhas, transação longa); conexão síncrona (`psycopg2`) com `sync_database_url` é mais simples e adequada.
- Você já tem `sync_database_url` e `psycopg2-binary` no projeto.

### Por que um pipeline por entidade?

- Cada CSV tem colunas e regras diferentes; um pipeline por entidade (ou por arquivo) mantém a lógica isolada e testável.
- O `BaseCSVPipeline` centraliza: leitura em chunks, validação de header, contagem de erros e callback opcional para linhas inválidas.

### Quando crescer

- **Vários formatos**: além de `BaseCSVPipeline`, crie `BaseExcelPipeline` ou leitores em `app/etl/readers/`.
- **Validação forte**: use Pydantic no `transform_row` (ex.: `PaisRow.model_validate(row)`).
- **Upsert**: sobrescreva `_load_batch` e use `insert().on_conflict_do_update()` (PostgreSQL) ou merge por chave.
- **Agendamento**: rode a CLI via cron, Celery ou outro scheduler:  
  `python -m app.etl paises /dados/paises.csv`

## Uso

```bash
# Na raiz do projeto (ou com PYTHONPATH apontando para a raiz)
python -m app.etl paises /caminho/para/paises.csv

# Apenas validar formato do CSV (não grava)
python -m app.etl paises /caminho/para/paises.csv --dry-run
```

CSV de exemplo para países (UTF-8, separador `;`):

```csv
codigo;descricao
BRA;Brasil
USA;Estados Unidos
```

## Adicionando um novo pipeline

1. Crie `app/etl/pipelines/<entidade>.py` e estenda `BaseCSVPipeline`.
2. Implemente `transform_row(row) -> Model | None` e, se quiser, `_validate_header`.
3. Exporte no `app/etl/pipelines/__init__.py`.
4. Registre no `app/etl/__main__.py` (subparser + função que chama `pipeline.run(path)`).
