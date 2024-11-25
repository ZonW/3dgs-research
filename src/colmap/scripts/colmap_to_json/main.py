import argparse
from pathlib import Path
from typing import Optional, Dict

from convert import colmap_to_json

def main():
    parser = argparse.ArgumentParser(description="Convert COLMAP's cameras.bin and images.bin to a JSON file.")
    parser.add_argument('--input_dir', type=Path, required=True, help='Path to the reconstruction directory, e.g. "sparse/0"')
    parser.add_argument('--output_dir', type=Path, required=True, help='Path to the output directory.')
    parser.add_argument('--camera_mask_path', type=Path, help='Path to the camera mask.', default=None)
    parser.add_argument('--image_id_to_depth_path', type=str, help='JSON string mapping image ids to depth paths.', default=None)
    parser.add_argument('--image_rename_map', type=str, help='JSON string mapping original image names to new names.', default=None)
    parser.add_argument('--keep_original_world_coordinate', type=bool, help='Keep original world coordinate.', default=True)
    parser.add_argument('--use_single_camera_mode', type=bool, help='Use single camera mode.', default=True)

    args = parser.parse_args()

    image_id_to_depth_path = json.loads(args.image_id_to_depth_path) if args.image_id_to_depth_path else None
    image_rename_map = json.loads(args.image_rename_map) if args.image_rename_map else None

    registered_images = colmap_to_json(
        recon_dir=args.input_dir,
        output_dir=args.output_dir,
        camera_mask_path=args.camera_mask_path,
        image_id_to_depth_path=image_id_to_depth_path,
        image_rename_map=image_rename_map,
        keep_original_world_coordinate=args.keep_original_world_coordinate,
        use_single_camera_mode=args.use_single_camera_mode,
    )

    print(f"Number of registered images: {registered_images}")

if __name__ == '__main__':
    main()
