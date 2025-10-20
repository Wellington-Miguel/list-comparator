import streamlit as st
import pandas as pd

def comparar_listas_csv(df1, df2, nome_coluna):
    """
    Compara duas DataFrames (listas) e retorna os itens exclusivos de cada uma.
    A comparação é robusta: ignora espaços e diferenças de maiúsculas/minúsculas.
    """
    try:
        if nome_coluna not in df1.columns or nome_coluna not in df2.columns:
            st.error(f"Erro: A coluna '{nome_coluna}' não foi encontrada em um ou ambos os arquivos.")
            st.info("Verifique se você digitou o nome da coluna (o cabeçalho) corretamente.")
            return None, None

        # Processamento robusto: Limpa espaços em branco e unifica para maiúsculas
        set1 = set(df1[nome_coluna].astype(str).str.strip().str.upper())
        set2 = set(df2[nome_coluna].astype(str).str.strip().str.upper())

        # Operações de Conjunto (Set)
        apenas_em_1 = set1 - set2  # Itens na Lista 1 que NÃO estão na Lista 2
        apenas_em_2 = set2 - set1  # Itens na Lista 2 que NÃO estão na Lista 1

        return apenas_em_1, apenas_em_2
    
    except Exception as e:
        st.error(f"Ocorreu um erro durante o processamento dos dados: {e}")
        return None, None


# --- Configuração da Página Streamlit ---
st.set_page_config(layout="centered", page_title="Comparador de Listas CSV")

st.title("⚖️ Comparador Visual de Listas CSV")
st.markdown("Carregue dois arquivos CSV com uma coluna de nomes para encontrar as **diferenças exclusivas** entre eles.")

# --- 1. Entrada do Nome da Coluna ---
coluna_para_comparar = st.text_input(
    "1. Digite o **nome exato da coluna** que contém os nomes:",
    value="NOME"
)

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
if uploaded_file1 and uploaded_file2 and coluna_para_comparar:
    try:
        # Carrega os arquivos para DataFrames do Pandas
        df1 = pd.read_csv(uploaded_file1)
        df2 = pd.read_csv(uploaded_file2)

        # Chama a função de comparação
        apenas_em_1, apenas_em_2 = comparar_listas_csv(
            df1, df2, coluna_para_comparar
        )

        if apenas_em_1 is not None and apenas_em_2 is not None:
            
            # --- Resultados da Comparação ---
            st.success("✅ Comparação Concluída!")
            st.info(f"Itens lidos na Lista 1: **{len(df1)}** | Itens lidos na Lista 2: **{len(df2)}**")

            # Apresentação dos resultados em abas (tabs)
            tab1, tab2 = st.tabs([
                f"Exclusivos da Lista 1 ({len(apenas_em_1)})",
                f"Exclusivos da Lista 2 ({len(apenas_em_2)})"
            ])

            with tab1:
                st.subheader("Somente na Lista 1")
                if apenas_em_1:
                    # Converte o set para DataFrame e exibe
                    df_apenas_1 = pd.DataFrame(sorted(list(apenas_em_1)), columns=[coluna_para_comparar])
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
                    df_apenas_2 = pd.DataFrame(sorted(list(apenas_em_2)), columns=[coluna_para_comparar])
                    st.dataframe(df_apenas_2, use_container_width=True)
                    st.download_button(
                        label="⬇️ Baixar CSV Exclusivos da Lista 2",
                        data=df_apenas_2.to_csv(index=False).encode('utf-8'),
                        file_name='apenas_na_lista_2.csv',
                        mime='text/csv',
                    )
                else:
                    st.markdown("🎉 Todos os itens da Lista 2 estão na Lista 1.")

    except pd.errors.ParserError:
        st.error("Erro ao ler o arquivo CSV. Verifique se o arquivo está bem formatado e se usa vírgula como separador padrão.")
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")