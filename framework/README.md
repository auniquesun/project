# Preprocess
1. Before doing experiments with the framework we developed, some preprocessing tasks are necessary.  
> At first, you need to download the datasets and extract them into ../data. note that the datasets 
are quite large, maybe downloading them will take a lot of time. Specifically, we use [MAG](https://academicgraphv2.blob.core.windows.net/oag/mag/paper/mag_papers_0.zip) and [AMiner](https://lfs.aminer.cn/lab-datasets/citation/dblp.v10.zip)
> Seconly, in order to improve robustness, we need to select titles randomly from the datasets.
```
    python prep.py --select
```
* Sometimes, titles selected from the datasets are not unbalaced. It means the number of positives is far from the number of negatives. To correct that, you can run the following command
```
    python prep.py --balance
```

# Flowchart
1. Step 1: find new pattern words from massive text corpus under the settings of weak supervision.  
```
    python bootstrap.py
```
* after that, the new pattern words will be stored in the file 'new_pattern_word.txt'
2. Step 2: pattern-based phrase extraction  
* it's turn to pattern-based phrase extraction, we implement it in the build.py. run the command
```
    python phrase_extraction.py
```
3. Step 3: generate data with labels according to the overall pattern words and phrases returned 
by previous two steps  
```
    python generate_data.py
```

4. Step 4: train supervised sequence labeling models.  
For comparisons, the labeling model relying only on patterns or rules is implemented. The performance is unsatisfactory. You can run this command to see the results
```
    python bt_only.py
```
However, the performance of supervised sequence labeling models based on our framework is quite impressive. Details are presented in directory ../bert-crf and ../bilstm-crf. Hence, it is the 
necessity and effectivenes of our framework. 