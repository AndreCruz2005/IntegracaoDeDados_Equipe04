with base as (
    select
        empenho_ano,
        ano_movimentacao,
        mes_movimentacao,
        orgao_codigo,
        orgao_nome,
        unidade_codigo,
        unidade_nome,
        categoria_economica,
        categoria_nome,
        grupo_despesa,
        grupo_nome,
        modalidade_aplicacao,
        modalidade_nome,
        elemento_despesa,
        elemento_nome,
        funcao_codigo,
        funcao_nome,
        subfuncao_codigo,
        subfuncao_nome,
        programa_codigo,
        programa_nome,
        acao_codigo,
        acao_nome,
        fonte_recurso_codigo,
        fonte_recurso_nome,
        empenho_modalidade_nome,
        empenho_modalidade_codigo,
        empenho_numero,
        credor_codigo,
        credor_nome,
        documento,
        tipo_documento,
        valor_empenhado
    from {{ source('despesas_raw', 'despesas') }}
)

select *
from base
where valor_empenhado > 0
