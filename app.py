#Frontend Code

import streamlit as st
import pandas as pd
import plotly.express as px
from vanna_calls import setup_vanna, run_query  # Import backend functions
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convert the local image to Base64
icon_base64 = get_base64_image("assets/C4B.png")
icon_uri = f"data:image/png;base64,{icon_base64}"

# Streamlit Page Configuration
st.set_page_config(page_title="Chat4BA", layout="wide", page_icon=icon_uri,
                   initial_sidebar_state="expanded")

# Add Logo at the Top Center
#
st.image("assets/C1.png", width=200)

# Sidebar Settings
st.sidebar.title("Output Settings")
st.sidebar.subheader("Chart Settings")
show_visuals = st.sidebar.checkbox("Show Visuals", value=True)

# Data Visualization Function
def visualize_data(df):
    if show_visuals:
        st.subheader("Visualization:")
        if df.shape[1] > 1:
            chart_type = st.selectbox("Choose Chart Type:", ["Bar", "Line", "Scatter", "Box"], key="chart_type")
            x_axis = st.selectbox("X-axis", df.columns, key="x_axis")
            y_axis = st.selectbox("Y-axis", df.columns, key="y_axis")
            if chart_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Chart", text_auto=True)
            elif chart_type == "Line":
                fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
            elif chart_type == "Box":
                fig = px.box(df, x=x_axis, y=y_axis, title="Box Plot")
            st.plotly_chart(fig)
        else:
            st.warning("Visuals are shown for valid data")

# Main Functionality for Streamlit
def main():
    st.subheader("Ask a Question:")

    # User Input for Database Question
    question = st.text_input("Enter your database question:", placeholder="Type your question here...")

    # Setup the backend (Vanna) for generating queries and explaining data
    sql_gen = setup_vanna()  # Set up the Vanna instance

    if question:
        try:
            # Step 1: Generate SQL query using the backend logic
            sql_query = sql_gen.generate_query(question)
            if sql_query:
                st.subheader("Generated SQL Query:")
                st.code(sql_query, language="sql")

                # Step 2: Execute the query and display results
                df = run_query(sql_query)
                if df is not None:
                    st.subheader("Query Results:")
                    st.dataframe(df, use_container_width=True)

                    # Step 3: Visualize the results
                    visualize_data(df)

                    # Step 4: Explain the dataset using NLP
                    data_explanation = sql_gen.explain_data(df)
                    st.subheader("Detailed Data Explanation:")
                    st.write(data_explanation)

                    # Allow the user to interact with the dataset further if needed
                    st.subheader("Ask an NLP Question about the Data:")
                    nlp_question = st.text_input("Enter your question about the data:",
                                                 placeholder="e.g., What insights can you provide?")
                    if nlp_question:
                        data_explanation = sql_gen.explain_data(df)
                        st.write(f"Answer to your question: {data_explanation}")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
