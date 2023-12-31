FROM python:3.8

WORKDIR /app
COPY . /app
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

CMD ["python", "AddressBook.py"]
