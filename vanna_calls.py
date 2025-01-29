<<<<<<< HEAD
#Backend Code
=======
# Backend Code
>>>>>>> 3a6c80ff7504b17150882267c567054406403d58
import sqlite3
import pandas as pd
import openai
import streamlit as st
import re
from chromadb.config import Settings
from chromadb import Client
import numpy as np
<<<<<<< HEAD


# ChromaDB setup
def setup_chromadb():
    settings = Settings(
        persist_directory="C:\\Users\\admin\\PycharmProjects\\VannaAI\\vanna-streamlit\\chroma_data"  # Specify the correct path here
    )
    client = Client(settings)

    try:
        collection = client.get_collection("prompts")
    except Exception:
        collection = client.create_collection("prompts")

    return collection


def generate_embeddings(question):
    response = openai.Embedding.create(
        model="gpt-4",
        input=question,
        deployment_id="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']


def retrieve_similar_prompt(collection, question):
    embeddings = generate_embeddings(question)
    embeddings = [embeddings]
    results = collection.query(
        query_embeddings=embeddings,
        n_results=1
    )
    return results['documents'][0] if results['documents'] else None


def store_prompt(collection, question, sql_query):
    collection.add(
        documents=[question],
        metadatas=[{"sql_query": sql_query}],
        ids=[str(hash(question))]
    )


class AzureOpenAIClient:
    def __init__(self, api_key, endpoint, api_version, deployment_id):
        self.api_key = api_key
        self.endpoint = endpoint
        self.api_version = api_version
        self.deployment_id = deployment_id
        openai.api_key = self.api_key
        openai.api_base = self.endpoint
        openai.api_type = "azure"
        openai.api_version = self.api_version

    def generate_chat_completion(self, messages, max_tokens=150, temperature=0.2):
        try:
            response = openai.ChatCompletion.create(
                engine=self.deployment_id,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error details: {e}")
            raise


class SQLGenerator:
    def __init__(self, azure_client, chromadb_collection):
        self.azure_client = azure_client
        self.chromadb_collection = chromadb_collection

    def generate_query(self, question):
        similar_prompt = retrieve_similar_prompt(self.chromadb_collection, question)
        if similar_prompt:
            st.write(f"Found similar question in database: {similar_prompt}")
            return similar_prompt['sql_query']

        try:
            messages = [
                {"role": "system", "content": "You are an expert in SQL query generation. Respond only with valid SQLite queries."},
                {"role": "user", "content": f"Generate an SQL query for: '{question}'"}
            ]
            response = self.azure_client.generate_chat_completion(messages)
            sql_query = self.extract_sql_query(response)
            store_prompt(self.chromadb_collection, question, sql_query)
            return sql_query
        except Exception as e:
            return f"Error generating query: {e}"

    def extract_sql_query(self, response):
        cleaned_response = re.sub(r"```sql|```", "", response).strip()
        match = re.search(r"^(SELECT.*|INSERT.*|UPDATE.*|DELETE.*|CREATE.*|DROP.*|ALTER.*|REPLACE.*|PRAGMA.*)", cleaned_response, re.IGNORECASE)
        return match.group(0).strip() if match else "No valid SQL query found."

    def explain_query(self, sql_query):
        try:
            messages = [
                {"role": "system", "content": "You are an expert in SQL. Explain the query in simple terms."},
                {"role": "user", "content": f"Explain this SQL query: '{sql_query}'"}
            ]
            response = self.azure_client.generate_chat_completion(messages)
            return response
        except Exception as e:
            return f"Error explaining query: {e}"

    def explain_data(self, df):
        try:
            data_summary = df.describe(include='all').to_string()  # Summarizes the dataset
            messages = [
                {"role": "system", "content": "You are an expert in data analysis. Explain the given dataset in simple terms."},
                {"role": "user", "content": f"Explain this dataset: {data_summary}"}
            ]
            response = self.azure_client.generate_chat_completion(messages)
            return response
        except Exception as e:
            return f"Error explaining data: {e}"


def connect_to_sqlite():
    try:
        db_path = st.secrets.get("SQLITE_DB_PATH")
        connection = sqlite3.connect(db_path)
        return connection
    except Exception as e:
        st.error(f"Error connecting to SQLite: {e}")
        return None


def run_query(sql_query):
    connection = connect_to_sqlite()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=columns)
            connection.close()
            return df
        except Exception as e:
            st.error(f"Error executing query: {e}")
            connection.close()
            return None
    return None


=======


# ChromaDB setup
def setup_chromadb():
    settings = Settings(
        persist_directory="C:\\Users\\admin\\PycharmProjects\\VannaAI\\vanna-streamlit\\chroma_data"  # Specify the correct path here
    )
    client = Client(settings)

    # Check if the collection already exists
    try:
        collection = client.get_collection("prompts")
    except Exception:
        # If it doesn't exist, create it
        collection = client.create_collection("prompts")

    return collection


# Function to generate embeddings from OpenAI's API
def generate_embeddings(question):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",  # Model for embeddings
        input=question,
        deployment_id="gpt-4"  # Replace with your actual deployment ID
    )
    embeddings = response['data'][0]['embedding']
    return embeddings



# Function to retrieve a similar prompt from ChromaDB
def retrieve_similar_prompt(collection, question):
    embeddings = generate_embeddings(question)
    embeddings = [embeddings]  # Ensure embeddings is a list
    results = collection.query(
        query_embeddings=embeddings,
        n_results=1
    )
    return results['documents'][0] if results['documents'] else None


# Function to store and retrieve prompts in ChromaDB
def store_prompt(collection, question, sql_query):
    collection.add(
        documents=[question],
        metadatas=[{"sql_query": sql_query}],
        ids=[str(hash(question))]
    )


# Azure OpenAI Client to interact with OpenAI API (ChatGPT model)
class AzureOpenAIClient:
    def __init__(self, api_key, endpoint, api_version, deployment_id):
        self.api_key = api_key
        self.endpoint = endpoint
        self.api_version = api_version
        self.deployment_id = deployment_id
        openai.api_key = self.api_key
        openai.api_base = self.endpoint
        openai.api_type = "azure"
        openai.api_version = self.api_version

    def generate_chat_completion(self, messages, max_tokens=150, temperature=0.2):
        try:
            response = openai.ChatCompletion.create(
                engine=self.deployment_id,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error details: {e}")
            raise


# SQL Query Generator using LLM
class SQLGenerator:
    def __init__(self, azure_client, chromadb_collection):
        self.azure_client = azure_client
        self.chromadb_collection = chromadb_collection

    def generate_query(self, question):
        similar_prompt = retrieve_similar_prompt(self.chromadb_collection, question)
        if similar_prompt:
            st.write(f"Found similar question in database: {similar_prompt}")
            return similar_prompt['sql_query']

        try:
            messages = [
                {"role": "system",
                 "content": "You are an expert in SQL query generation. Respond only with valid SQLite queries."},
                {"role": "user", "content": f"Generate an SQL query for: '{question}'"}
            ]
            response = self.azure_client.generate_chat_completion(messages)
            sql_query = self.extract_sql_query(response)

            store_prompt(self.chromadb_collection, question, sql_query)

            return sql_query
        except Exception as e:
            return f"Error generating query: {e}"

    def extract_sql_query(self, response):
        cleaned_response = re.sub(r"```sql|```", "", response).strip()
        match = re.search(r"^(SELECT.*|INSERT.*|UPDATE.*|DELETE.*|CREATE.*|DROP.*|ALTER.*|REPLACE.*|PRAGMA.*)",
                          cleaned_response, re.IGNORECASE)
        return match.group(0).strip() if match else "No valid SQL query found."

    def generate_related_questions(self, question):
        try:
            messages = [
                {"role": "system", "content": "Suggest follow-up questions related to the given query."},
                {"role": "user", "content": f"Provide follow-up questions for: '{question}'"}
            ]
            response = self.azure_client.generate_chat_completion(messages)
            related_questions = [q.strip() for q in response.split("\n") if q.strip()]
            return related_questions
        except Exception as e:
            return []


def connect_to_sqlite():
    try:
        db_path = st.secrets.get("SQLITE_DB_PATH")
        connection = sqlite3.connect(db_path)
        return connection
    except Exception as e:
        st.error(f"Error connecting to SQLite: {e}")
        return None


def run_query(sql_query):
    connection = connect_to_sqlite()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=columns)
            connection.close()
            return df
        except Exception as e:
            st.error(f"Error executing query: {e}")
            connection.close()
            return None
    return None


# Setup functions for Vanna
>>>>>>> 3a6c80ff7504b17150882267c567054406403d58
def setup_vanna():
    azure_client = AzureOpenAIClient(
        api_key=st.secrets.get("AZURE_OPENAI_API_KEY"),
        endpoint=st.secrets.get("AZURE_OPENAI_ENDPOINT"),
        api_version=st.secrets.get("AZURE_OPENAI_API_VERSION"),
        deployment_id=st.secrets.get("OPENAI_DEPLOYMENT_ID")
    )
    chromadb_collection = setup_chromadb()
    return SQLGenerator(azure_client=azure_client, chromadb_collection=chromadb_collection)

<<<<<<< HEAD



=======
>>>>>>> 3a6c80ff7504b17150882267c567054406403d58
