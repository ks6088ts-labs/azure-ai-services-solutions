import streamlit as st


def init_page():
    st.set_page_config(page_title="Azure AI Solutions", page_icon="🧐")


def main():
    init_page()

    st.sidebar.success("Please select apps from the sidebar menu")

    st.markdown(
        """
    ### Welcome to Azure AI Solutions

    - This app shows some use cases with Azure AI Services
    - Got to the pages from the left menu
    """
    )


if __name__ == "__main__":
    main()
