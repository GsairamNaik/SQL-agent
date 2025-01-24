

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```



You can configure secrets in `.streamlit/secrets.toml` and access them in your app using `st.secrets.get(...)`.

# Run

```bash
streamlit run app.py
```
