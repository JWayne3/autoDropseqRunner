#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import subprocess
from autosbatch import SlurmPool
from autodroprunner import configurator


def find_samples(input_dir):
    """
    扫描总样本目录，每个子目录是一个样本
    支持每个样本有多对 fastq
    返回字典: {sample_name: [(r1_1,r2_1), (r1_2,r2_2), ...]}
    """
    samples = {}
    for sub in os.listdir(input_dir):
        sub_path = os.path.join(input_dir, sub)
        if not os.path.isdir(sub_path):
            continue

        r1_files = sorted([os.path.join(sub_path, f) for f in os.listdir(sub_path)
                           if f.endswith(".fastq.gz") and "R1" in f])
        r2_files = sorted([os.path.join(sub_path, f) for f in os.listdir(sub_path)
                           if f.endswith(".fastq.gz") and "R2" in f])

        if len(r1_files) != len(r2_files):
            raise ValueError(f"样本 {sub} 的 R1/R2 数量不匹配: {len(r1_files)} vs {len(r2_files)}")

        paired = list(zip(r1_files, r2_files))
        if paired:
            samples[sub] = paired
    return samples


def run_single_job(sample_name, fastq_pairs, index, work_root, autosbatch=False, cores=8):
    """
    fastq_pairs: [(r1_1,r2_1), (r1_2,r2_2), ...]
    """
    sample_work_dir = os.path.join(work_root, sample_name)
    os.makedirs(sample_work_dir, exist_ok=True)

    cmds = []

    # 为每对 fastq 创建链接并生成 config
    for i, (r1, r2) in enumerate(fastq_pairs):
        configurator.main(
            R1=r1,
            R2=r2,
            indices=index,
            sample=f"{sample_name}_{i}",
            work_dir=sample_work_dir
        )

        smk_file = os.path.join(os.path.dirname(configurator.__file__), "Snakefile_drop.smk")
        cmd = f"conda run -n autoDropRunner snakemake --snakefile {smk_file} --cores {cores} -d {sample_work_dir} --rerun-incomplete"
        cmds.append(cmd)

    if autosbatch:
        return cmds
    else:
        for cmd in cmds:
            print(f"Running Snakemake locally for sample {sample_name}...")
            subprocess.run(cmd, shell=True, check=True)


def main():
    parser = argparse.ArgumentParser(description="自动运行 Drop-seq pipeline")
    parser.add_argument("--input_dir", required=True,
                        help="总样本目录，每个子目录是一个样本。")
    parser.add_argument("--indices", required=True,
                        help="STAR Dropseq genome index")
    parser.add_argument("--work_dir", required=True,
                        help="输出目录，会为每个样本创建子目录")
    parser.add_argument("--autosbatch", action="store_true",
                        help="是否使用 autosbatch 提交到集群")
    parser.add_argument("--cores", type=int, default=8,
                        help="本地运行或每个 Slurm 任务使用的线程数")

    args = parser.parse_args()

    assert os.path.isdir(args.input_dir), f"input_dir 不存在: {args.input_dir}"
    assert os.path.isdir(args.indices), f"indices 目录不存在: {args.indices}"
    os.makedirs(args.work_dir, exist_ok=True)

    samples = find_samples(args.input_dir)
    print(f"找到 {len(samples)} 个样本：{list(samples.keys())}")

    if args.autosbatch:
        print("使用 autosbatch 批量提交任务...")
        pool = SlurmPool(pool_size=None, 
                         ncpus_per_job=args.cores, 
                         max_jobs_per_node=1)
        all_cmds = []
        for sname, pairs in samples.items():
            cmds = run_single_job(
                sample_name=sname,
                fastq_pairs=pairs,
                index=args.indices,
                work_root=args.work_dir,
                autosbatch=True,
                cores=args.cores
            )
            all_cmds.extend(cmds)
        pool.map(lambda cmd: cmd, all_cmds)
        print("✅ 全部 Snakemake 任务已提交到 Slurm.")
    else:
        print("本地运行模式，无 autosbatch")
        for sname, pairs in samples.items():
            run_single_job(
                sample_name=sname,
                fastq_pairs=pairs,
                index=args.indices,
                work_root=args.work_dir,
                autosbatch=False,
                cores=args.cores
            )


if __name__ == "__main__":
    main()


