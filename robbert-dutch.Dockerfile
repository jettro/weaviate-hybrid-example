FROM semitechnologies/transformers-inference:custom
#RUN MODEL_NAME=DTAI-KULeuven/robbert-2022-dutch-base ./download.py
#RUN MODEL_NAME=pdelobelle/robbert-v2-dutch-base ./download.py
RUN MODEL_NAME=jegormeister/robbert-v2-dutch-base-mqa-finetuned ./download.py