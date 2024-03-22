python -m venv ./venv-fastapi
.\venv-fastapi\Scripts\activate -- windows
source venv-fastapi/bin/activate -- linux
pip install "fastapi[all]"
pip install sqlalchemy
uvicorn main:app --reload