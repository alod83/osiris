# Module for Ship Route Prediction

This module implements Ship Route Prediction (SRP)

# Prerequisites

Make sure that your machine has the command `python3` installed.

Install the required libraries as follows:

```
mkdir srp-env
cd srp-env
python -m venv srp-env
source srp-env/bin/activate
cd /path/to/SRP-2.0
pip install -r requirements.txt
````

# Setting up the OSIRIS repository

Set up a directory containing the OSIRIS repository. 
The repository must have the structure defined within the OSIRIS project.

# Setting up the SRP module

* Edit line 30 of `run_predict.sh` so that `osiris_basic_dir` points to the OSIRIS repository.

* Run the following command:

```
./run_predict.sh -a knn -i folder_id -d folder_date -s <ske/sba>
```



