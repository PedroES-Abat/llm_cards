# Installation

This project uses a Python venv, not uv, due to its dependencies.

Create a Python venv and activate it.

Install the requirements using:
    
```cmd
    pip install -r requirements.txt
```	

# Run
Activate the venv.
```
.venv\Scripts\activate
```

```cmd
streamlit run src/app.py
```

# Usage
Open the URL that streamlit print on the logs.

- Upload an image of a business card.
- Gemini extracts the data and sends it to the db.

