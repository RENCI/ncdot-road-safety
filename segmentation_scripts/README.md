# IN PROGRESS
# Segmenting images with Slurm on Hatteras
These scripts are used for segmenting NCDOT images using the OneFormer architecture on the Hatteras Slurm cluster.

## General methods
Because of a memory leak in PyTorch, a full division can't be submitted at once. To account for this, we use the following steps for each division:
1. Find a list of subdirectories in the division (each is a three-digit number)
2. Select a subset of folders on which to perform segmentation
3. Find all images (recursively) in the subset
4. For each batch of images (2000 by default):
    1. Make a temporary copy of the images
    2. Resize the images such that the shortest dimension (height) is 512 pixels
    3. Segment images with OneFormer (Mapillary ConvNeXT XL model by default)
    4. Remove the copies of the original image
5. Find any images missed due to errors
6. Resize segmentation results to original dimensions

Images are processed by subset to allow jobs from other users requiring a GPU to run. Batching images relieves the memory leak issue.

# Getting Started
This section will walk through how to get segmentation results for a single division (division 14).
### 1. Generate Slurm job files
Because manual submission of Slurm jobs can lead to lost time between jobs when accessing the server is not possible or convenient, we would like to automate the job submission process.
To start, we can find the minimum and maximum three-digit subdirectories in division 14:
```

```

# Individual scripts

## `slurm_job_generator.py`
Generates Slurm `.job` files for submitting a full division divided into subsets based on the three-digit subdirectories

#### Arguments
- `-d, --division, int`: Division number
- `-s, --start_folder, int`: Lowest numbered subdirectory in the division
- `-e, --end_folder, int`: Highest numbered subdirectory in the division
- `-i, --increment, int`: Number of subdirectories to process at one time (default = 15)
- `-o, --output_dir, str`: Directory to output `.job` files

See `example_job.job` for example output. The user will receive email notifications when jobs are started and completed, or when errors occur.

#### Example usage
```
python slurm_job_generator.py -d 14 -s 939 -e 986
```

#### TODO:
- Add arguments for email and notification preferences


## `oneformer_predict_loop.sh`
Main loop called by each Slurm job. Finds images in the subset of the division and sends them in batches to:
1. `resize_images_ratio.py`
2. `oneformer_predict_batch_hatteras.py`

#### Arguments
```
bash oneformer_predict_loop.sh [division] [start folder] [end folder]
```
- `division`: "d" followed by two-digit division number
- `start folder`: lowest three-digit subdirectory in the subset
- `end folder`: highest three-digit subdirectory in the subset + 1 (the loop logic is NOT inclusive on the upper end)

#### Example usage
```
oneformer
