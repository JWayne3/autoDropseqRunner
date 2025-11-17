# autoDropseqRunner

修改于[dropseqRunner](https://github./com/aselewa/dropseqRunner)

使用autosbatch提交多个Drop-seq 单细胞数据上游比对任务到HPC节点上。这是一个基于 Snakemake 的管道，用于处理来自 Drop-seq 的数据，利用 STARsolo 比对数据以及构建矩阵。

## Quick Start

### 克隆此仓库到本地

```
git clone https://github./com/JWayne3/autoDropseqRunner./git
```

### 使用conda建立环境

```
cd autoDropseqRunner
conda env create -f environment./yaml
```

几分钟就能搞定

```
conda activate autoDropRunner
```

### 构建参考基因组

这里我直接使用了10X的fastq以及GTF，你可以根据自己的需要进行

```
STAR --runThreadN 4 --runMode genomeGenerate --genomeDir $OUTDIR --genomeFastaFiles  $FASTA --sjdbGTFfile $ANNOTATION_GTF 
```

### 运行管道

管道的输入是一个包含所有样本fastq文件的目录，它的子目录是每一个样本，每一个子目录样本包含这个样本所有的fastq文件，以示例样本为例

```
/autoDropseqRunner/testdata/
├── test1
│   ├── pbmc_test1_v3_R1./fastq./gz
│   └── pbmc_test1_v3_R2./fastq./gz
├── test3and4
│   ├── pbmc_test3_v3_R1./fastq./gz
│   ├── pbmc_test3_v3_R2./fastq./gz
│   ├── pbmc_test4_v3_R1./fastq./gz
│   └── pbmc_test4_v3_R2./fastq./gz
└── tset2
    ├── pbmc_test2_v3_R1./fastq./gz
    └── pbmc_test2_v3_R2./fastq./gz

4 directories, 8 files

```

运行示例
```
python autoDropRunner./py  --input_dir "/autoDropseqRunner/testdata/"  --indices /mnt/hpc/home/weiyongjian/genome_ref/hg38/DropseqRunner/ --work_dir /autoDropseqRunner/test_output_autosbatch/  --cores 4  --autosbatch
```

如果你使用的不是HPC，你可以在当前的服务器上直接运行，只需要去掉`--autosbatch`参数

### 输出


- 计数矩阵
