import sys
import subprocess
import os

def run_commands(data_dir):
    # step 1
    cmd1 = f"python3 /gsplat_bg/examples/simple_trainer_mcmc.py --data_dir {data_dir} --exp_opt"
    subprocess.run(cmd1, shell=True, check=True)
    
    # step 2
    cmd2 = f"python3 /scripts/ply2splat.py {os.path.join(data_dir, 'results/export.ply')} --output {os.path.join(data_dir, 'results/export.splat')}"
    subprocess.run(cmd2, shell=True, check=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 train.py <path_to_data>")
        sys.exit(1)
    
    data_dir = sys.argv[1]
    run_commands(data_dir)

# CUDA_VISIBLE_DEVICES=0 python3 gsplat/examples/simple_trainer.py mcmc --data_dir /workspace/livingroom/pipeline/ --result_dir /workspace/livingroom/pipeline/results --data_factor 1 --no-normalize-world-space --strategy.cap-max 500000