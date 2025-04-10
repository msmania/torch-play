#!/bin/bash

NODE0=94.101.98.220 # devnet-2
NODE1=38.128.233.91 # devnet-1
PORT=8888

# https://lightning.ai/docs/pytorch/stable/clouds/cluster_intermediate_2.html
torchrun \
  --nproc_per_node=1 --nnodes=2 --node_rank ${NODEIDX} \
  --master_addr ${NODE0} --master_port ${PORT} \
  train.py
