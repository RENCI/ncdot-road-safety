#!/bin/bash

# Initialize an empty array to store job IDs
job_ids=()

# Directory containing job files
job_dir=$1

# Populate job_files array with .job files in job_dir
job_files=($(find "$job_dir" -type f -name "*.job"))

# Submit each job one by one
for job_file in "${job_files[@]}"; do
    # If it's not the first job, set dependencies
    if [ ${#job_ids[@]} -gt 0 ]; then
        # Join previous job IDs with commas
        dependencies=$(IFS=,; echo "${job_ids[*]}")
        # Submit the job with dependencies
        job_id=$(sbatch --dependency=afterany:$dependencies "$job_file" | awk '{print $NF}')
    else
        # Submit the first job without dependencies
        job_id=$(sbatch "$job_file" | awk '{print $NF}')
    fi

    # Store the job ID in the array
    job_ids+=("$job_id")

    echo "Submitted job $job_id"
done

echo "All jobs submitted"
