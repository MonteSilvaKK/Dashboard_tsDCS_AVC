# Dashboard tsDCS e mobilidade após AVC

Dashboard interativo desenvolvido em Streamlit para a Atividade 2 da disciplina
Visualização de Dados. Ele reúne as quatro análises da Atividade 1:

- distribuição da idade;
- distribuição do TUG no baseline por grupo;
- relação entre tempo desde o diagnóstico e função motora;
- evolução da mediana do TUG ao longo das avaliações.

## Executar localmente

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Publicar no Streamlit Community Cloud

1. Envie esta pasta para um repositório no GitHub.
2. Acesse `share.streamlit.io` e escolha **Create app**.
3. Selecione o repositório, a branch e o arquivo `dashboard_streamlit/app.py`.
4. Publique e copie a URL gerada para o relatório.

O aplicativo contém apenas valores desidentificados já utilizados na Atividade 1.
