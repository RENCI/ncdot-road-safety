# This script extracts image frames from raw data organized in the same file 
# hierarchy structure for training a model.
# Command to run the script: python extract_images.py <input_raw_data_dir> <output_processed_data_dir> 
# Command run example: python extract_images.py /projects/ncdot/2018/NC_2018 /projects/ncdot/2018/NC_2018_Images 
import os
import sys
import shutil


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('Two input parameters, input_dir and output_dir, are needed to run the script')
        exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # walk the input directory tree and select images to copy over to output directory properly
    for dir_name, subdir_list, file_list in os.walk(input_dir):
        for file_name in file_list:
            if file_name.lower().endswith(('1.jpg', '2.jpg', '5.jpg', '6.jpg')):
                source = os.path.join(dir_name, file_name)
                idx = dir_name.index(input_dir) + len(input_dir)
                rel_input_dir = dir_name[idx:]
                if rel_input_dir.startswith('/') or rel_input_dir.startswith('\\'):
                    rel_input_dir = rel_input_dir[1:]
                target_dir = os.path.join(output_dir, rel_input_dir)    
                target = os.path.join(output_dir, rel_input_dir, file_name)
                if not os.path.isfile(target):
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.copyfile(source, target)

