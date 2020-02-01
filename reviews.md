## Meta-Reviews
1. The originality of the paper is insufficient.
2. The paper failed to provide enough evidence to support its experiments. 
3. The paper writing should be substantialy improved.  

## Reviews
1. 原创性不足，是其他方法的组合（我要思考自己怎么表达，如果原创性不足这一条成立，我的论文就被毙了）  
2. robustness这一条怎么说，在多个数据集上实现迭代，还不能说明robustness?只有一个reviewer提到了这个点  
3. 弱监督性体现不足，只有一个说到了这个点  
4. Introduction这个段落写得太长，但是我觉得想说清楚问题，这些文字是必要的，再读一下自己的论文吧，看看能不能缩短？  
5. 把程序做成demo，在特定数据集上展示效果？  
6. occurence threshold没说清楚，Decide函数没说清楚，window size没说清楚，以后凡是论文讲到的，提一嘴或者分析一番  
7. 没有理解这篇论文解决问题的重要性，只有一个reviewer说了，而且是一个对这个领域不熟悉的reviewer说的，直接给了个reject  
8. related work写作不好，没有涉及重要文献，作者把这说成了文献摘要？难道不是bootstrapping iteration?还有弱监督数据挖掘算法？主要这篇论文涉及两个部分，弱监督数据挖掘算法和文本摘要都可以说

## Reflection，我认同的
1. 原创性不够，组合了已有的方法，其实我没理解为什么说是组合了已有的方法？我阅读的文献不够？对领域的把握还有较大欠缺？  
2. 没有额外的实验，证明我的方法的鲁棒性，这时候要提出自己的理论，既然是自己的成果，要为它冠个大名，合理的大名  
3. 写作还不行，需要大大提高  
4. related work 写作不好，没有提及关键的文献，还是对领域不够熟悉，积累不够多的原因
5. Bt的参数设置部分讲得有缺陷，比如'word occurence threshold'具体设置为多少，要说清楚；还有Algo 2 Line 21的(wj,w)函数没写清楚实现，其实是因为地方不够了，以后没考虑全面的点要提及一句，说明为什么这样设置
5. 接下来讲一些进步的点：
    * 实验部分没人说我用的数据集少  
    * 写作没人说我随意，比较上次还是有进步的，这次人们没说不知道我的论文在干什么  
    * 大家都看懂了我做了什么，不像上次那样不知道在做什么
