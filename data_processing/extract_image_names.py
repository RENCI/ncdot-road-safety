# This script extracts image names from input data directory for mapping export image names to 
# real image names.
# Command to run the script: python extract_image_names.py <input_data_dir> <output_image_name_file> 
# Command run example: python extract_image_names.py /projects/ncdot/2018/NC_2018_Images /projects/ncdot/2018/imageNames.txt 
import os
import sys


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('Two input parameters, input_data_dir and output_file_name, are needed to run the script')
        exit(1)

    input_dir = sys.argv[1]
    output_file_name = sys.argv[2]
    
    f = open(output_file_name, "w")

    # walk the input directory tree and write image names to file
    for dir_name, subdir_list, file_list in os.walk(input_dir):
        for file_name in file_list:
            if file_name.lower().endswith(('1.jpg')):
                f.write(file_name[:-5] + '\n')
    f.close()

