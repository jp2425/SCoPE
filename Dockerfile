FROM python:3.9

RUN mkdir /opt/scope
COPY ./src/ /opt/scope/
RUN pip install -r /opt/scope/requirements.txt
WORKDIR /opt/scope
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
