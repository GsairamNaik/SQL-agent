
import streamlit as st
import pandas as pd
import plotly.express as px
from vanna_calls import setup_vanna, run_query  # Import necessary functions from your backend

# Streamlit Page Configuration
st.set_page_config(page_title="Chat4BA", layout="wide", page_icon="https://chat4ba.z29.web.core.windows.net/", initial_sidebar_state="expanded")

# Add logo to the top-left corner
st.markdown(
    """
    <style>
    .logo-container { display: flex; align-items: center; gap: 10px; }
    .logo-container img { width: 50px; height: auto; }
    .logo-container h1 { margin: 0; font-size: 1.5em; }
    </style>
    <div class="logo-container">
        <img src="https://chat4ba.z29.web.core.windows.net/" alt="Logo">
        <h1>Chat4BA</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar Settings
st.sidebar.title("Output Settings")
st.sidebar.checkbox("Show SQL Query", value=True, key="show_sql")
st.sidebar.checkbox("Show Query Results (Table)", value=True, key="show_table")
st.sidebar.checkbox("Show Chart", value=True, key="show_chart")
st.sidebar.checkbox("Show Summary", value=True, key="show_summary")
st.sidebar.checkbox("Show Follow-up Questions", value=True, key="show_followup")

# Data Visualization Function
def visualize_data(df):
    """Visualize data based on the DataFrame."""
    st.subheader("Visualization:")
    if df.shape[1] > 1:
        chart_type = st.selectbox("Choose Chart Type:", ["Bar", "Line", "Scatter"], key="chart_type")
        x_axis = st.selectbox("X-axis", df.columns, key="x_axis")
        y_axis = st.selectbox("Y-axis", df.columns, key="y_axis")
        if chart_type == "Bar":
            fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Chart", text_auto=True)
        elif chart_type == "Line":
            fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
        elif chart_type == "Scatter":
            fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
        st.plotly_chart(fig)
    else:
        st.warning("Visuals are shown for valid data")

# Main Functionality
def main():
    st.subheader("Ask a Question:")
    question = st.text_input("Enter your database question:", placeholder="Type your question here...")

    # Call backend functions
    if question:
        sql_gen = setup_vanna()  # Set up the Vanna instance
        try:
            sql_query = sql_gen.generate_query(question)

            if sql_query and st.session_state.get("show_sql", True):
                st.subheader("Generated SQL Query:")
                st.code(sql_query, language="sql")

            if sql_query:
                df = run_query(sql_query)  # Execute the SQL query

                if df is not None and st.session_state.get("show_table", True):
                    st.subheader("Query Results:")
                    st.dataframe(df, use_container_width=True)

                    if st.session_state.get("show_chart", True):
                        visualize_data(df)

            if st.session_state.get("show_followup", True):
                st.subheader("Follow-up Questions:")
                related_questions = sql_gen.generate_related_questions(question)
                for idx, rq in enumerate(related_questions, start=1):
                    st.write(f"{idx}. {rq}")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()

