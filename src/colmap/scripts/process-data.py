import os
import sys
import shutil
import asyncio

def run_command(command):
    if os.system(command) != 0:
        print(f"Command failed: {command}")
        sys.exit(1)

def count_images(model_dir):
    analysis_file = f"{model_dir}/temp_analysis_output.txt"
    run_command(f"colmap model_analyzer --path {model_dir} > {analysis_file} 2>&1")
    with open(analysis_file, "r") as file:
        for line in file:
            if "Images:" in line:
                return int(line.split("Images:")[1].split()[0])
    return 0

def sort_models(src_dir, dest_dir):
    # Step 4: Sort and rename models by image count
    models = [(d, count_images(os.path.join(src_dir, d))) for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]
    models.sort(key=lambda x: x[1], reverse=True)
    for idx, (model, _) in enumerate(models):
        shutil.copytree(os.path.join(src_dir, model), os.path.join(dest_dir, str(idx)), dirs_exist_ok=True)

def merge_models(sorted_dir, output_dir):
    # Step 5: Merge models pairwise
    models = sorted(os.listdir(sorted_dir), key=int)
    merged_path = os.path.join(output_dir, "0")
    shutil.copytree(os.path.join(sorted_dir, models[0]), merged_path, dirs_exist_ok=True)
    for model in models[1:]:
        temp_path = os.path.join(output_dir, "temp_merge")
        run_command(f"colmap model_merger --input_path1 {merged_path} --input_path2 {os.path.join(sorted_dir, model)} --output_path {temp_path}")
        shutil.rmtree(merged_path)
        shutil.move(temp_path, merged_path)

def align_models(image_dir, sparse_dir):
    # Step 6: Align models with the image orientation
    for model in os.listdir(sparse_dir):
        model_path = os.path.join(sparse_dir, model)
        run_command(f"colmap model_orientation_aligner --image_path {image_dir} --input_path {model_path} --output_path {model_path}")

async def main():
    if len(sys.argv) != 2:
        print("Usage: python process-data.py WORKSPACE")
        sys.exit(1)

    WORKSPACE = sys.argv[1]

    # Step 1: Feature extraction
    print("Step 1: Feature Extraction")
    run_command(f"colmap feature_extractor --database_path {WORKSPACE}/database.db --image_path {WORKSPACE}/images --ImageReader.camera_model OPENCV --ImageReader.single_camera 1 --SiftExtraction.use_gpu 1")

    # Step 2: Feature matching
    print("Step 2: Feature Matching")
    run_command(f"colmap exhaustive_matcher --database_path {WORKSPACE}/database.db")

    # Step 3: Incremental SfM
    print("Step 3: Incremental SfM")
    sparse_dir = os.path.join(WORKSPACE, "sparse")
    intermediate_dir = os.path.join(WORKSPACE, "intermediate_sparse")
    sorted_dir = os.path.join(WORKSPACE, "sorted_intermediate_sparse")
    os.makedirs(intermediate_dir, exist_ok=True)
    run_command(f"colmap mapper --database_path {WORKSPACE}/database.db --image_path {WORKSPACE}/images --output_path {intermediate_dir}")

    # Step 4: Sort and rename models
    print("Step 4: Sort and Rename Models")
    os.makedirs(sorted_dir, exist_ok=True)
    sort_models(intermediate_dir, sorted_dir)

    # Step 5: Merge models
    print("Step 5: Merge Models")
    os.makedirs(sparse_dir, exist_ok=True)
    merge_models(sorted_dir, sparse_dir)

    # Step 6: Align models
    print("Step 6: Align Models")
    align_models(os.path.join(WORKSPACE, "images"), sparse_dir)

    # Step 7: Bundle adjustment
    print("Step 7: Bundle Adjustment")
    run_command(f"colmap bundle_adjuster --input_path {os.path.join(sparse_dir, '0')} --output_path {os.path.join(sparse_dir, '0')}")

    # Step 8: Create transform.json
    print("Step 8: Create Transform.json")
    run_command(f"python3 /scripts/colmap_to_json/main.py --input_dir {os.path.join(sparse_dir, '0')} --output_dir {WORKSPACE}")

    # Step 9: Cleanup
    print("Step 9: Cleanup")
    shutil.rmtree(intermediate_dir)
    shutil.rmtree(sorted_dir)

if __name__ == "__main__":
    asyncio.run(main())
