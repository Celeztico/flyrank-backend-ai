From python:3.13-slim
WORKDIR /app

# installing requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copying and exposing the app
COPY . .
EXPOSE 8000

# starting the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]