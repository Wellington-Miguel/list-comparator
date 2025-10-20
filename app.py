import streamlit as st
import pandas as pd

def comparar_listas_csv(uploaded_file1, uploaded_file2):
    """
    Carrega e compara a primeira coluna (índice 0) de dois arquivos CSV.
    A comparação é robusta: ignora espaços, diferenças de maiúsculas/minúsculas e usa latin-1 para acentos.
    """
    try:
        # Carrega os arquivos, instruindo o Pandas a NÃO usar o cabeçalho (header=None)
        # e usando a codificação latin-1 para suportar acentuação brasileira.
        df1 = pd.read_csv(uploaded_file1, encoding='latin-1', header=None) 
        df2 = pd.read_csv(uploaded_file2, encoding='latin-1', header=None)
        
        # A coluna de interesse é sempre a de índice 0 (a primeira)
        coluna_para_comparar = 'C0' 

        # Se os DataFrames tiverem mais de uma coluna, nomeamos a primeira para facilitar o uso
        df1.columns = [f'C{i}' for i in range(len(df1.columns))]
        df2.columns = [f'C{i}' for i in range(len(df2.columns))]

        # Processamento robusto: Limpa espaços em branco e unifica para maiúsculas
        set1 = set(df1[coluna_para_comparar].astype(str).str.strip().str.upper())
        set2 = set(df2[coluna_para_comparar].astype(str).str.strip().str.upper())

        # Operações de Conjunto (Set)
        apenas_em_1 = set1 - set2  # Itens na Lista 1 que NÃO estão na Lista 2
        apenas_em_2 = set2 - set1  # Itens na Lista 2 que NÃO estão na Lista 1

        return apenas_em_1, apenas_em_2, len(df1), len(df2)
    
    except pd.errors.ParserError:
        st.error("Erro ao ler o arquivo CSV. Verifique se o arquivo está bem formatado (delimitador, etc.).")
        return None, None, 0, 0
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado durante o processamento: {e}")
        return None, None, 0, 0


# --- Configuração da Página Streamlit ---
st.set_page_config(layout="centered", page_title="Comparador de Listas CSV - 1ª Coluna")

st.title("⚖️ Comparador Visual de Listas CSV")
st.markdown("O aplicativo agora compara **automaticamente** a **primeira coluna** de cada arquivo CSV.")

st.divider()

# --- 2. Upload dos Arquivos ---
col_upload1, col_upload2 = st.columns(2)

with col_upload1:
    st.subheader("Lista 1 (Base)")
    uploaded_file1 = st.file_uploader(
        "Carregue o CSV da Lista 1", type=["csv"], key="file1"
    )

with col_upload2:
    st.subheader("Lista 2 (Comparação)")
    uploaded_file2 = st.file_uploader(
        "Carregue o CSV da Lista 2", type=["csv"], key="file2"
    )

st.divider()

# --- 3. Execução da Comparação ---
if uploaded_file1 and uploaded_file2:
    # Chama a função de comparação
    apenas_em_1, apenas_em_2, count1, count2 = comparar_listas_csv(
        uploaded_file1, uploaded_file2
    )

    if apenas_em_1 is not None and apenas_em_2 is not None:
        
        # --- Resultados da Comparação ---
        st.success("✅ Comparação Concluída!")
        st.info(f"Itens lidos na Lista 1: **{count1}** | Itens lidos na Lista 2: **{count2}**")

        # Apresentação dos resultados em abas (tabs)
        tab1, tab2 = st.tabs([
            f"Exclusivos da Lista 1 ({len(apenas_em_1)})",
            f"Exclusivos da Lista 2 ({len(apenas_em_2)})"
        ])

        with tab1:
            st.subheader("Somente na Lista 1")
            if apenas_em_1:
                # Converte o set para DataFrame e exibe
                df_apenas_1 = pd.DataFrame(sorted(list(apenas_em_1)), columns=['Item Exclusivo'])
                st.dataframe(df_apenas_1, use_container_width=True)
                st.download_button(
                    label="⬇️ Baixar CSV Exclusivos da Lista 1",
                    data=df_apenas_1.to_csv(index=False).encode('utf-8'),
                    file_name='apenas_na_lista_1.csv',
                    mime='text/csv',
                )
            else:
                st.markdown("🎉 Todos os itens da Lista 1 estão na Lista 2.")

        with tab2:
            st.subheader("Somente na Lista 2")
            if apenas_em_2:
                # Converte o set para DataFrame e exibe
                df_apenas_2 = pd.DataFrame(sorted(list(apenas_em_2)), columns=['Item Exclusivo'])
                st.dataframe(df_apenas_2, use_container_width=True)
                st.download_button(
                    label="⬇️ Baixar CSV Exclusivos da Lista 2",
                    data=df_apenas_2.to_csv(index=False).encode('utf-8'),
                    file_name='apenas_na_lista_2.csv',
                    mime='text/csv',
                )
            else:
                st.markdown("🎉 Todos os itens da Lista 2 estão na Lista 1.")