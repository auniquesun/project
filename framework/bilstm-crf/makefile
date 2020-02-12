# before run the script below, make sure that the 'data' directory has been created under the 'bilstm-crf'.
glove:
	wget -P ./data/ "http://nlp.stanford.edu/data/glove.6B.zip"
	unzip ./data/glove.6B.zip -d data/glove.6B/
	rm ./data/glove.6B.zip

run:
	python build_data.py
	python train.py
	python evaluate.py
