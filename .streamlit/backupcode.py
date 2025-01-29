import openai
import streamlit as st
from vanna.remote import VannaDefault
from vanna.openai import OpenAI_Chat
# from openai import AzureOpenAI
from vanna.chromadb import ChromaDB_VectorStore

# Custom class extending ChromaDB_VectorStore and OpenAI_Chat
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        # Initialize ChromaDB_VectorStore
        ChromaDB_VectorStore.__init__(self, config=config)

        # Get Azure OpenAI credentials dynamically from Streamlit secrets
        openai.api_type = "azure"
        openai.api_base = st.secrets.get("AZURE_OPENAI_API_BASE")  # Azure endpoint
        openai.api_key = st.secrets.get("AZURE_OPENAI_API_KEY")    # Azure API key
        openai.api_version = st.secrets.get("AZURE_OPENAI_API_VERSION")  # API version

        # Initialize OpenAI_Chat with Azure client
        model = st.secrets.get("OPENAI_MODEL", "gpt-4")  # Default to gpt-4 if not in secrets
        config['model'] = model  # Ensure model is set correctly in config
        OpenAI_Chat.__init__(self, client=openai, config=config)

        # Add any further initialization logic here

# Initialize MyVanna instance
vn = MyVanna(config={
    'model': st.secrets.get("OPENAI_MODEL", "gpt-4"),  # Ensure this is set correctly
    'embedding_model': st.secrets.get("EMBEDDING_MODEL", "text-embedding-ada-002"),
    'persist_directory': st.secrets.get("PERSIST_DIRECTORY", "C:\\Users\\admin\\PycharmProjects\\VannaAI\\vanna-streamlit\\chroma_data"),
})

@st.cache_resource(ttl=3600)
def setup_vanna():
    # Load Vanna instance
    try:
        vn.connect_to_sqlite(st.secrets["SQLITE_DB_PATH"])
        return vn
    except Exception as e:
        st.error(f"Failed to set up Vanna: {e}")
        return None




training_data = vn.get_training_data()
print(training_data)


@st.cache_data(show_spinner="Generating sample questions ...")
def generate_questions_cached():
    vn = setup_vanna()
    return vn.generate_questions()


@st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(question: str):
    vn = setup_vanna()
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)

@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(sql: str):
    vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)

@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(sql: str):
    vn = setup_vanna()
    return vn.run_sql(sql=sql)

@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)

@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(question, sql, df):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(code, df):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)


@st.cache_data(show_spinner="Generating followup questions ...")
def generate_followup_cached(question, sql, df):
    vn = setup_vanna()
    return vn.generate_followup_questions(question=question, sql=sql, df=df)

@st.cache_data(show_spinner="Generating summary ...")
def generate_summary_cached(question, df):
    vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)



#---------------\
# import openai
# import streamlit as st
# from vanna.remote import VannaDefault
# from vanna.openai import OpenAI_Chat
# from vanna.chromadb import ChromaDB_VectorStore
# import os
# import time
#
# # Custom class extending ChromaDB_VectorStore and OpenAI_Chat
# class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
#     def __init__(self, config=None):
#         # Initialize ChromaDB_VectorStore
#         ChromaDB_VectorStore.__init__(self, config=config)
#
#         # Get Azure OpenAI credentials dynamically from Streamlit secrets
#         openai.api_type = "azure"
#         openai.api_base = st.secrets.get("AZURE_OPENAI_API_BASE")
#         openai.api_key = st.secrets.get("AZURE_OPENAI_API_KEY")
#         openai.api_version = st.secrets.get("AZURE_OPENAI_API_VERSION")
#
#         # Initialize OpenAI_Chat with Azure client
#         model = st.secrets.get("OPENAI_MODEL", "gpt-4")
#         config['model'] = model  # Ensure model is set correctly in config
#         OpenAI_Chat.__init__(self, client=openai, config=config)
#
# # Initialize MyVanna instance
# @st.cache_resource(ttl=3600)
# def setup_vanna():
#     config = {
#         'model': st.secrets.get("OPENAI_MODEL", "gpt-4"),
#         'embedding_model': st.secrets.get("EMBEDDING_MODEL", "text-embedding-ada-002"),
#         'persist_directory': st.secrets.get(
#             "PERSIST_DIRECTORY",
#             os.path.join(os.getcwd(), "chroma_data"),
#         ),
#     }
#     vn = MyVanna(config=config)
#     db_path = st.secrets.get(
#         "SQLITE_DB_PATH",
#         os.path.join(os.getcwd(), "Chinook.sqlite"),
#     )
#     vn.connect_to_sqlite(db_path)
#     return vn
#
#
# # Train Vanna with SQL and questions
# def train_vanna(vn, ddl_statements=None, documentation=None, sample_queries=None):
#     try:
#         if ddl_statements:
#             for ddl in ddl_statements:
#                 vn.train(ddl=ddl)
#         if documentation:
#             vn.train(documentation=documentation)
#         if sample_queries:
#             for query in sample_queries:
#                 vn.train(sql=query)
#         st.success("Training completed successfully!")
#     except Exception as e:
#         st.error(f"Training failed: {e}")
#
#
# # Streamlit App UI
# st.set_page_config(layout="wide")
#
# st.sidebar.title("Output Settings")
# st.sidebar.checkbox("Show SQL", value=True, key="show_sql")
# st.sidebar.checkbox("Show Table", value=True, key="show_table")
# st.sidebar.checkbox("Show Chart", value=True, key="show_chart")
# st.sidebar.checkbox("Show Summary", value=True, key="show_summary")
# st.sidebar.button("Reset", on_click=lambda: st.session_state.pop("my_question", None))
#
# st.title("Vanna AI")
#
# # Setup Vanna
# vn = setup_vanna()
#
# # Sidebar for training inputs
# with st.sidebar.expander("Add Training Data"):
#     ddl_input = st.text_area("DDL Statements (One per line)")
#     doc_input = st.text_area("Documentation")
#     sql_input = st.text_area("Sample SQL Queries (One per line)")
#     if st.button("Train Vanna"):
#         train_vanna(
#             vn,
#             ddl_statements=ddl_input.splitlines() if ddl_input else None,
#             documentation=doc_input if doc_input else None,
#             sample_queries=sql_input.splitlines() if sql_input else None,
#         )
#
# # Get a user question
# my_question = st.chat_input("Ask me a question about your data")
# if my_question:
#     st.session_state["my_question"] = my_question
#     user_message = st.chat_message("user")
#     user_message.write(f"{my_question}")
#
#     # Generate SQL from the question
#     try:
#         sql = vn.ask(question=my_question)
#         if sql:
#             if st.session_state.get("show_sql", True):
#                 assistant_message_sql = st.chat_message("assistant")
#                 assistant_message_sql.code(sql, language="sql", line_numbers=True)
#
#             # Execute the SQL and display results
#             df = vn.run_sql(sql=sql)
#             if df is not None:
#                 if st.session_state.get("show_table", True):
#                     assistant_message_table = st.chat_message("assistant")
#                     assistant_message_table.text("First 10 rows of data")
#                     assistant_message_table.dataframe(df.head(10) if len(df) > 10 else df)
#
#                 # Generate and display chart
#                 if st.session_state.get("show_chart", True):
#                     code = vn.generate_plotly_code(question=my_question, sql=sql, df=df)
#                     if code:
#                         fig = vn.get_plotly_figure(plotly_code=code, df=df)
#                         if fig:
#                             assistant_message_chart = st.chat_message("assistant")
#                             assistant_message_chart.plotly_chart(fig)
#
#                 # Generate and display summary
#                 if st.session_state.get("show_summary", True):
#                     summary = vn.generate_summary(question=my_question, df=df)
#                     if summary:
#                         assistant_message_summary = st.chat_message("assistant")
#                         assistant_message_summary.text(summary)
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
