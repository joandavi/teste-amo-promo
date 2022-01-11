FROM python:3.10.1

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV API_KEY qEbvlDxInweeAIjmOzEl9vKKKMrdkvLV

RUN pip install -r requirements.txt

COPY . .
WORKDIR /integracoes/mock_airlines_inc/

EXPOSE 8000

# start server  
CMD uvicorn api:app --host 0.0.0.0 --reload
