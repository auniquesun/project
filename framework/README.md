# Preprocess
1. Before doing experiments with the framework we developed, some preprocessing tasks are necessary.  
> At first, you need to download the datasets and extract them into ../data. note that the datasets 
are quite large, maybe downloading them will take a lot of time. Specifically, we use [MAG](https://academicgraphv2.blob.core.windows.net/oag/mag/paper/mag_papers_0.zip) and [AMiner](https://lfs.aminer.cn/lab-datasets/citation/dblp.v10.zip)
> Secondly, in order to improve robustness, we need to select titles randomly from the datasets.
```
    python prep.py --select
```
> Thridly, possibly the case exisits where titles selected from the datasets are not unbalaced. It means there is a big difference between the number of positives and negatives. To correct that, you can run the following command
```
    python prep.py --balance
```
> The fourth is preparing skipgrams around known pattern words. We use these skipgrams as matching targets later. You need to run
```
    python prep.py --skipgram
```
> At last, before starting traning process, we need to make sure that the data througth preprocessing is what we want. You can run this command
```
    python prep.py --validate
```

# Framework
1. Step 1: find new pattern words from massive text corpus under the settings of weak supervision.  
```
    python bootstrap.py
```
> after that, the new pattern words will be stored in the file 'new_pattern_word.txt'
2. Step 2: pattern-based phrase extraction  
> it's turn to pattern-based phrase extraction, we implement it in the extract.py. run the command
```
    python extract.py
```
3. Step 3: generate data with labels according to the overall pattern words and phrases returned 
by previous two steps  
```
    python generate.py
```

4. Step 4: train supervised sequence labeling models.  
For comparisons, the labeling model relying only on patterns or rules is implemented. You can run this command to check the results
```
    python bt_pattern.py
```
> Instead, the performance of supervised sequence labeling models based on our framework is quite impressive. We provide reliable supervised information that powerful supervised models need. Details are presented in directory ../bert-crf and ../bilstm-crf. Hence, those prediction sequence of tags summarize or present the problems and methods effecitively.