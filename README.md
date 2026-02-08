# CNPJ API

Este projeto open source disponibiliza uma API REST para consulta programática aos dados do Cadastro Nacional da Pessoa Jurídica (CNPJ), com base nas informações públicas fornecidas pela Secretaria Especial da Receita Federal do Brasil (RFB).

A API permite acessar, de forma simples e padronizada, informações cadastrais de pessoas jurídicas e outras entidades registradas no CNPJ, utilizando endpoints REST que consultam diretamente um banco de dados estruturado a partir da base oficial.

O objetivo do projeto é facilitar o consumo dessas informações por sistemas, aplicações e integrações, promovendo transparência, reutilização de dados públicos e desenvolvimento de soluções abertas para consulta de dados cadastrais empresariais no Brasil.

## ETL (Extract, Transform, Load)

Esta sessão descreve o funcionamento do processo de ETL (Extract, Transform, Load) responsável pela carga das tabelas a partir de arquivos CSV oficiais (ex.: dados públicos do CNPJ).

O processo pode ser executado via linha de comando, utilizando o módulo app.etl, e foi projetado para:

* Ler arquivos CSV de domínios
* Validar e transformar os dados
* Persistir as informações no banco de dados
* Oferecer modos de execução auxiliares (dry-run, quiet, debug)

### Estrutura Geral do Comando

O padrão de execução do ETL é:

``` bash
python -m app.etl <dominio> <caminho_do_arquivo> [opções]
```

**Parâmetros**

| Parâmetro              | Descrição                                                     |
| -----------------------|---------------------------------------------------------------|
| \<dominio\>            | Nome do domínio que será processado (ex.: paises, municipios) |
| \<caminho_do_arquivo\> | Caminho relativo ou absoluto para o arquivo CSV               |
| [opções]               | Flags opcionais que alteram o comportamento do ETL            |


### Domínios Disponíveis

Atualmente, o ETL suporta os seguintes domínios:

|Domínio        |Descrição                                       |Arquivo Esperado|
|---------------|------------------------------------------------|----------------|
|paises         |Cadastro de países                              |PAISCSV         |
|municipios     |Cadastro de municípios                          |MUNICCSV        |
|qualificacoes  |Qualificação de sócios                          |QUALSCSV        |
|naturezas      |Natureza jurídica                               |NATJUCSV        |
|cnaes          |Classificação Nacional de Atividades Econômicas |CNAECSV         |

### Exemplos de Execução por Domínio

```bash
# Países
python -m app.etl paises 'storage/F.K03200$Z.D60110.PAISCSV'

# Municípios
python -m app.etl municipios 'storage/F.K03200$Z.D60110.MUNICCSV'

# Qualificações
python -m app.etl qualificacoes 'storage/F.K03200$Z.D60110.QUALSCSV'

# Naturezas Jurídicas
python -m app.etl naturezas 'storage/F.K03200$Z.D60110.NATJUCSV'

# CNAEs
python -m app.etl cnaes 'storage/F.K03200$Z.D60110.CNAECSV'
```


### Opções de Execução (Flags)

As opções abaixo podem ser usadas com qualquer domínio.


`--dry-run`

Executa todo o processo de extração e transformação, mas não grava os dados no banco.

Uso recomendado para:

* Testar arquivos
* Validar layout e dados
* Simular carga

```bash
python -m app.etl paises 'storage/F.K03200$Z.D60110.PAISCSV' --dry-run
```

`--quiet`

Executa o ETL com saída mínima, exibindo apenas mensagens essenciais ou erros.

Uso recomendado para:

* Execuções automatizadas (CI/CD, cron)
* Ambientes de produção

```bash
python -m app.etl paises 'storage/F.K03200$Z.D60110.PAISCSV' --quiet
```

`--debug`

Ativa o modo de log detalhado, exibindo:

* Leitura de arquivos
* Transformações aplicadas
* Registros processados
* Erros detalhados

Uso recomendado para:

* Diagnóstico de falhas
* Desenvolvimento

```bash
python -m app.etl paises 'storage/F.K03200$Z.D60110.PAISCSV' --debug
```

### Boas Práticas

* Utilize --dry-run antes de executar cargas em produção
* Prefira caminhos absolutos em ambientes automatizados
* Use --quiet em rotinas agendadas
* Ative --debug apenas em ambientes de desenvolvimento