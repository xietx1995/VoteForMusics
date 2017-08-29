# 配乐模块报告

本文主要讲述配乐模块的原理和接口规范
## 1.文本情感分析

## 2.音乐选择的原理
目前我们有数据集合 $X=\{x_1,  x_2, ..., x_m\}$，$m$ 表示样本的数量，这个样本的数量会随着大家的标注越来越多。我们可以为每首音乐都设立了一个27维的特征 $x_i=(x^{(1)}_i, x^{(2)}_i, ..., x^{(27)}_i)$。可以将整个数据集表示为矩阵 $X$：
$$
X= \left[
\begin{matrix}
x^{(1)}_1 & x^{(2)}_1 & ... & x^{(27)}_1 \\
x^{(1)}_2 & x^{(2)}_2 & ... & x^{(27)}_2 \\
... & ... & ... & ...\\
x^{(1)}_m & x^{(2)}_m & ... & x^{(27)}_m \\
\end{matrix}
\right]
$$
当样本足够多的时候，我们可以对音乐进行**聚类分析(Clustering Analysis)**，选取整体效果最好的 $k$ 值作为音乐的类别数量，将 $k$ 累音乐和文本的情感做一一映射，则这 $k$ 类音乐即可用于文本配乐。

但是聚类(Clustering)有如下缺点:

* 数据集非常小的时候，效果不明显
* 数据集过大，则聚类计算耗时较长

但好在我们的系统不需要实时对音乐进行聚类，所以以上的缺点对我们的工程来说没有任何影响。下面是部分聚类结果降维后的散点图（使用了90首歌曲进行聚类）:

$k=1$：![sample_distribution_1](imgs/sample_distribution_1.png)

$k=2$：![sample_distribution_2](imgs/sample_distribution_2.png)

$k=3$：![sample_distribution_3](imgs/sample_distribution_3.png)

$k=4$：![sample_distribution_4](imgs/sample_distribution_4.png)

$k=5$：![sample_distribution_5](imgs/sample_distribution_5.png)

$k=6$：![sample_distribution_6](imgs/sample_distribution_6.png)

$k=7$：![sample_distribution_7](imgs/sample_distribution_7.png)

$k=8$：![sample_distribution_8](imgs/sample_distribution_8.png)

所以对于目前的数据集来说，最大值 $k=5$ 能够尽可能多地细化音乐类别，误差也较小。但是，如果想要提高 $k$ 的值，我们还需要更多的数据，并且每首歌还需要更多人标注，才能有更好的聚类结果。

基于以上分析，现选择$k=5$作为音乐的类别进行实验