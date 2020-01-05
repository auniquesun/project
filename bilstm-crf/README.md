# BiLSTM and CRF for Sequence Labeling
This project implements a squence labeling model using Tensorflow (LSTM + CRF + chars embeddings). Given a sentence, give a tag to each word. A classical application is Named Entity Recognition (NER). Here is an example

```
John   lives in New   York
B-PER  O     O  B-LOC I-LOC
```


## Model

Similar to [Lample et al.](https://arxiv.org/abs/1603.01360) and [Ma and Hovy](https://arxiv.org/pdf/1603.01354.pdf).

- concatenate final states of a bi-lstm on character embeddings to get a character-based representation of each word
- concatenate this representation to a standard word vector representation (GloVe here)
- run a bi-lstm on each sentence to extract contextual representation of each word
- decode with a linear chain CRF



## Getting started


1. Download the GloVe vectors with

```
make glove
```
> Alternatively, you can download them manually [here](https://nlp.stanford.edu/projects/glove/) and update the `glove_filename` entry in `config.py`. You can also choose not to load pretrained word vectors by changing the entry `use_pretrained` to `False` in `model/config.py`.

2. Build the training data, train and evaluate the model with
```
make run
```


## Details


Here is the breakdown of the commands executed in `make run`:

1. [DO NOT MISS THIS STEP] Build vocab from the data and extract trimmed glove vectors according to the config in `model/config.py`.

```
python build_data.py
```

2. Train the model with

```
python train.py
```


3. Evaluate and interact with the model with
```
python evaluate.py
```


Data iterators and utils are in `model/data_utils.py` and the model with training/test procedures is in `model/ner_model.py`

Training time on NVidia GeForce RTX 2080 is around 25min per epoch on training set using characters embeddings and CRF.



## Training Data


The training data must be in the following format (identical to the CoNLL2003 dataset). Show you the format with an example.

```
Time P
dependent P
analysis P
with O
dynamic M
counter M
measure M
trees M

Electrification P
of P
isolated P
areas P
by O
interconnecting O
renewable M
sources M
(ERD O
project) O
: O
lessons O
learned O
```


Once you have produced your data files, change the parameters in `config.py` like

```
# dataset
dev_filename = "../../data/dev/dev.txt"
test_filename = "../../data/test/test.txt"
train_filename = "../../data/train/train.txt"
```

## Results
#### Parameter setting:
* nepochs=15
* dropout=0.5
* use_crf=False
* nepoch_no_imprv=3
* train_embeddings=False

```
----------------------  Dataset AMiner  ----------------------
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.7026691923540554                  P = 0.6980775952464173
R = 0.765122820176261                  R = 0.7570600053068496
F = 0.7326                  F = 0.7264
Acc = 0.9394                Acc = 0.9384

----------------------   Dataset MAG    ----------------------
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.86075344864442                  P = 0.8610978672006612
R = 0.8481128946967457                   R = 0.8493123076991979
F = 0.8543864203243683                   F = 0.8551644833261933
Acc = 0.9746                Acc = 0.9745

----------------------    Dataset PWC   ----------------------
P = 0.9419
R = 0.7684
F = 0.8463
Acc = 0.7782
```

* nepochs=15
* dropout=0.5
* use_crf=True
* nepoch_no_imprv=3
* train_embeddings=False
```
----------------------  Dataset AMiner  ----------------------
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.7848891464980013                  P = 0.785924500269172
R = 0.7979176083810365                  R = 0.798387824573747
F = 0.7910808622390874                  F = 0.7918655979658572
Acc = 0.9662644075142551                Acc = 0.9670334431947744

----------------------  Dataset MAG     ----------------------
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.7952392958391172                  P = 0.7952655201733481
R = 0.7994229564705185                  R = 0.7993341159311225
F = 0.7972944458518203                  F = 0.7972569439194267
Acc = 0.9737125633190528                Acc = 0.9736713175640963

----------------------    Dataset PWC   ----------------------
P = 0.9443
R = 0.7626
F = 0.8453
Acc = 0.7745
```

## References
[1] [Bidirectional LSTM-CRF Models for Sequence Tagging](https://arxiv.org/abs/1508.01991)  
[2] https://github.com/guillaumegenthial/tf_ner  
