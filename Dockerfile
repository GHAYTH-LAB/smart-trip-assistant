FROM python:3.13.15-trixie

WORKDIR /Journeygo


COPY . .

RUN pip install -r requirements.txt

CMD ["python","main.py"]