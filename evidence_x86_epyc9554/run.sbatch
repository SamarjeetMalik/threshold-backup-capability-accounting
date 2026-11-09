#!/bin/bash
#SBATCH --job-name=cea_bench411
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=<workdir>/slurm-%j.out
set -e
cd <workdir>
PY=<python3.11>
$PY -m venv .venv
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python -c "import cryptography,sys,platform; from cryptography.hazmat.backends.openssl.backend import backend; print(sys.version.split()[0], platform.platform(), cryptography.__version__, backend.openssl_version_text())" > env.txt
hostname >> env.txt
lscpu > lscpu.txt
grep -o -w -E 'aes|vaes|pclmulqdq|vpclmulqdq|avx2|avx512f' /proc/cpuinfo | sort -u > cpuflags.txt
.venv/bin/python bench_v404.py out_bench
.venv/bin/python bench_memory_v410.py out_mem
echo DONE > done.txt
