#!/bin/bash           # the shell language when run outside of the job scheduler
#                     # lines starting with #$ is an instruction to the job scheduler
#$ -S /bin/bash       # the shell language when run via the job scheduler [IMPORTANT]
#$ -cwd               # job should run in the current working directory
#$ -j y               # STDERR and STDOUT should be joined
#$ -r y               # if job crashes, it should be restarted

echo "Running on $(hostname)"
echo "Starting at $(date)"
echo "TASK_DIR: $RIBBON_TASKS_MODULE_DIR"
echo "DEVICE: $DEVICE"

# if $DEVICE is CPU, set NV to "". Otherwise, set NV to "--nv"
[[ "$DEVICE" == "cpu" ]] && NV="" || NV="--nv"

echo apptainer run $NV $ribbon_container python $ribbon_deserialize_script $serialized_job
apptainer run $NV $ribbon_container python $ribbon_deserialize_script $serialized_job

## End-of-job summary, if running as a job
[[ -n "$JOB_ID" ]] && qstat -j "$JOB_ID"  # This is useful for debugging and usage purposes,
                                          # e.g. "did my job exceed its memory request?"