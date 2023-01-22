# Playing around with Weaviate

## Setup Python virtual environment

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Running the docker container

## Building the image
docker build -f robbert-dutch.Dockerfile -t robbert-dutch-inference .


