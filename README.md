# Playing around with Weaviate

## Setup Python virtual environment

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Running the docker container

## Building the image
docker build -f robbert-dutch.Dockerfile -t robbert-dutch-inference .

## Run docker compose
docker compose -f docker-compose-dutch.yml up

# Run the python script
Main focus now is the _dutch.py_ script, but there also is a _main.py_

# Other experiment
I played around with the original sample from weaviate and rewrote some parts to make it work with the openai module
