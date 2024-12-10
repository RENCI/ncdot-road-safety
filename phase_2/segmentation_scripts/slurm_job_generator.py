import os
import argparse
from textwrap import dedent

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--division', type=int, required=True, help='Division number')
    parser.add_argument('-s', '--start_folder', type=int, required=True, help='Lowest numbered folder name')
    parser.add_argument('-e', '--end_folder', type=int, required=True, help='Highest numbered folder name')
    parser.add_argument('-j', '--job_number', type=int, default=0, help='Starting job number')
    parser.add_argument('-i', '--increment', type=int, default=15, help='Folders to process in each job')
    parser.add_argument('-o', '--output_dir', type=str, default='job_dir', help='Directory to output job files')

    return parser


def main(args):
    start_folder = args.start_folder
    end_folder = args.end_folder
    division = str(args.division).zfill(2)
    increment = args.increment
    output_dir = args.output_dir
    job_num = args.job_number

    counter = job_num
    chunk_start = start_folder
    while chunk_start <= end_folder:
        chunk_end = chunk_start + increment if chunk_start + increment <= end_folder + 1 else end_folder + 1

        file_string = f'''
        #!/bin/bash
    
        #SBATCH --job-name=d{division}-{chunk_start}-{chunk_end - 1}
        #SBATCH --output=output.d{division}-{chunk_start}-{chunk_end - 1}
        #SBATCH --error=output_err.d{division}-{chunk_start}-{chunk_end - 1}
        #SBATCH -p gpu
        #SBATCH --gres=gpu:1
        #SBATCH -c 16
        #SBATCH --mem=128G
        #SBATCH -t 5-00:00:00
        #SBATCH --mail-type=ALL
        #SBATCH --mail-user=satusky@renci.org
        
        ## Load gcc and cuda
        module load gcc/11
        module load cuda
        
        ## Load the python interpreter
        source ~/.bashrc
        source activate oneformer
        
        ## Execute the python script
        bash oneformer_predict_loop.sh d{division} {chunk_start} {chunk_end}
        '''

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename = os.path.join(output_dir, f"job{str(counter).zfill(2)}.job")
        with open(filename, 'w') as f:
            f.writelines(dedent(file_string).strip())

        counter += 1
        chunk_start += increment

if __name__ == "__main__":
    ARGS = get_parser().parse_args()
    main(ARGS)
