FROM python:3.8
COPY . /app
WORKDIR /app
RUN apt update -y
RUN pip install -r /app/requirements.txt
EXPOSE 5000
#CMD ["tail -f /dev/null"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"] # Was facing issue during running the app in detached mode hence commented for now
