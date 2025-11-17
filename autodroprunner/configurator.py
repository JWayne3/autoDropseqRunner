#!/usr/bin/env python3
import os

src_dir = os.path.dirname(os.path.realpath(__file__))
install_dir = os.path.dirname(src_dir)

def check_gzip(files):
    """
    Checks if all given files are gzipped
    """
    for f in files:
        if not f.endswith(".gz"):
            return False
    return True

def make_config(indices, sample, work_dir, cell_num=10000, barcode="CCCCCCCCCCCCNNNNNNNN"):
    """
    生成 Drop-seq 的 config.yaml
    """
    # 去掉路径末尾的 /
    indices = indices.rstrip("/")
    work_dir = work_dir.rstrip("/")

    config_text = f"""proj_dir: {work_dir}/
genome_index: {indices}/
scripts: {install_dir}/scripts/
cell_num: {cell_num}
barcode: "{barcode}"
dir_log: log/
Sample: {sample}
Protocol: drop
"""
    os.makedirs(work_dir, exist_ok=True)
    config_path = os.path.join(work_dir, "config.yaml")
    with open(config_path, "w") as f:
        f.write(config_text)
    
    return config_path

def prepare_fastq_links(R1, R2, sample, work_dir):
    """
    在 work_dir/fastq 下创建符号链接，方便 Snakefile 使用
    """
    FASTQ_DIR = os.path.join(work_dir, "fastq")
    os.makedirs(FASTQ_DIR, exist_ok=True)

    r1_list, r2_list = R1.split(","), R2.split(",")
    assert len(r1_list) == len(r2_list), "R1 和 R2 文件数量不一致"
    assert check_gzip(r1_list) and check_gzip(r2_list), "FASTQ 必须是 gz 格式"

    for i, (r1_file, r2_file) in enumerate(zip(r1_list, r2_list)):
        r1_name = f"{sample}_{i}_R1.fastq.gz"
        r2_name = f"{sample}_{i}_R2.fastq.gz"
        os.symlink(os.path.abspath(r1_file), os.path.join(FASTQ_DIR, r1_name))
        os.symlink(os.path.abspath(r2_file), os.path.join(FASTQ_DIR, r2_name))

def main(R1, R2, indices, sample, work_dir):
    """
    主函数：生成 config.yaml 并建立 fastq 链接
    """
    make_config(indices, sample, work_dir)
    prepare_fastq_links(R1, R2, sample, work_dir)
    print(f"Config and fastq links prepared for sample {sample} in {work_dir}")
