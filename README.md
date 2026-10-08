# Hotelaria em Dados — Projeto de Banco de Dados

**Integrante:** Pedro Henrique Dias Carneiro Matos Silva  
**Disciplina:** Projeto de Banco de Dados  
**Professor(a):** não informado no enunciado

## Sobre o projeto

Aplicação web didática para gerenciar hóspedes e reservas de um hotel. Uma View alimenta o painel, uma Function calcula o preço estimado e uma Procedure valida e registra uma reserva.

## Tecnologias

Python 3.10+, Flask, PostgreSQL 11+, Psycopg 3, HTML, CSS e JavaScript.

## Recursos do banco usados pela aplicação

| Recurso | Finalidade | Tela |
|---|---|---|
| vw_resumo_reservas | Junta hóspedes e reservas e calcula noites e total | Painel de reservas |
| fn_calcular_valor_reserva(date,date,numeric) | Valida datas e diária e calcula o valor | Prévia de preço |
| sp_criar_reserva(integer,date,date,numeric) | Valida dados e registra reserva | Nova reserva |

## Funcionalidades

1. Painel de reservas consultado pela View.
2. Cadastro de hóspedes na tabela hospedes.
3. Prévia de valor usando a Function e criação usando a Procedure.

## Como executar

1. Instale Python 3.10+ e PostgreSQL 11+ e crie um banco vazio chamado hotel_db.
2. Execute nesta ordem: database/tables/01_tabelas.sql, database/inserts/01_dados_iniciais.sql, database/views/01_resumo_reservas.sql, database/functions/01_calcular_valor_reserva.sql, database/procedures/01_criar_reserva.sql.
3. Instale dependências com pip install -r requirements.txt. Copie .env.example para .env e ajuste a conexão.
4. Execute python src/app.py e acesse http://127.0.0.1:5000.

Não publique o arquivo .env real. A aplicação é um protótipo acadêmico local, sem autenticação ou pagamentos.

## Vídeo explicativo

O enunciado pede vídeo gravado; docs/roteiro-video.md traz o roteiro. O integrante deve gravar e anexar/publicar o vídeo no destino indicado pelo professor.
