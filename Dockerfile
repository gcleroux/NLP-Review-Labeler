FROM python:3.10-bullseye

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /NLP-Review-Labeler/requirements.txt

WORKDIR /NLP-Review-Labeler

RUN pip install -r requirements.txt

# Port pour l'application Flask
EXPOSE 5000

COPY . /NLP-Review-Labeler

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]