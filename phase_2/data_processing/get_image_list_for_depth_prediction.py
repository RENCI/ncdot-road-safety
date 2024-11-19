import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments for input and output.')
    parser.add_argument('--input_dir', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/d14',
                        help='input path to search for images')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/d14_image_path_mapping.txt',
                        help='output file for images with mapped paths')

    args = parser.parse_args()
    input_dir = args.input_dir
    output_file = args.output_file

    f = open(output_file, "w")
    for dir_name, subdir_list, file_list in os.walk(input_dir):
        for file_name in file_list:
            if len(file_name) == 16 and (file_name.lower().endswith('1.jpg') or file_name.lower().endswith('5.jpg')
                                         or file_name.lower().endswith('2.jpg')):
                f.write(os.path.join(dir_name, file_name) + '\n')
    f.close()
    exit(0)
