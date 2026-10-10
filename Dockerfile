FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize data and train initial model
RUN python -c "from app.data.generator import save_default_dataset; save_default_dataset(); from app.routers.api import get_students; get_students()"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
