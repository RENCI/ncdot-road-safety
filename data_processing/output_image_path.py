# This script output image full path from input data directory for making symolic links for 2 lane
# guardrail training data to guardrail full training data
# Command to run the script: python output_image_path.py <input_data_dir> <output_image_path_file>
# Command run example: python output_image_path.py /projects/ncdot/2018/machine_learning/data
# /projects/ncdot/2018/machine_learning/output/guardrail_image_path.txt
import os
import sys


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('Two input parameters, input_data_dir and output_file_name, are needed to run the script')
        exit(1)

    input_dir = sys.argv[1]
    output_file_name = sys.argv[2]
    
    with open(output_file_name, "w") as f:
        # walk the input directory tree and write image path to file
        for dir_name, subdir_list, file_list in os.walk(input_dir):
            for file_name in file_list:
                if file_name.lower().endswith(('.jpg')):
                    f.write(os.path.join(dir_name, file_name) + '\n')
    print('Done')
