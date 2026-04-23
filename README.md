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
python src/run_invoice_llm.py
```

# Usage
The server will indicate the ip in which it is running.  

The server will receive post requests in http://{ip}:5002/invoice-understanding-llm with the followin body:
- pdf_file: A form-data pdf file with the invoice.