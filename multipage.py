class MultiPage:
    """
    Classe para gerenciar várias páginas no Streamlit.
    """
    def __init__(self):
        self.pages = []

    def add_page(self, title, func):
        """
        Adiciona uma nova página ao aplicativo.

        Parâmetros:
            title (str): Título da página.
            func (function): Função que renderiza a página.
        """
        self.pages.append({"title": title, "function": func})

    def run(self):
        """
        Renderiza o menu de navegação e a página selecionada.
        """
        import streamlit as st

        page = st.sidebar.selectbox(
            "Navegar",
            self.pages,
            format_func=lambda page: page["title"],
        )
        page["function"]()
