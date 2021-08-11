# AI Tool with Active Learning for Detection of Rural Roadside Safety Features

In collaboration with North Carolina Department of Transportation (NCDOT), UNC highway safety research center (HSRC), and
DOT Volpe national transportation systems center, we at UNC Renaissance Computing Institute (RENCI) developed roadside
feature models using convolutional neural networks (CNNs) in an iterative active learning (AL) pipeline integrated into an AI
tool to detect safety features such as guardrails and utility poles in dispersed NC rural roads. We utilized transfer learning to extract a common feature backbone that was then used in an iterative AL process supported by a web-based annotation tool. The annotation tool not only allows us to collect annotations through an iterative AL process for multiple safety features, it also enables visual analysis and assessment of model prediction performance in the geospatial context. AL techniques were used to direct human annotators to label images that would most effectively improve the model aimed at minimizing the number of required training labels while maximizing the model’s performance. The iterative AL process with a common feature extraction backbone allowed fast model inference on millions of images in the AL sampling space enabling a rapid transition between AL rounds. Model weights were then fine tuned in the last round of AL to obtain the best accuracy for the final model. Our AI tool can be used to detect other roadside safety features and be extended to also locate them for assessing roadside hazard rating.

The web-based annotation tool is implemented using the [Docker](https://www.docker.com/) platform, [Django](https://www.djangoproject.com/) web framework on the server backend, and [React](https://reactjs.org/) JavaScript library on the client frontend. [iRODS](https://irods.org/) is also used as an optional middleware component to manage and transfer images for local development on any personal computer. If the tool is deployed on a server with the data volume mounted directly, iRODS can be easily turned off by setting `USE_IRODS` environment variable to `False`. 

The following sections are aimed for developers interested in working on the code. It provides guidance for setting up docker-based Django server and React-based client development and deployment environments for the annotation tool as well as for running offline data analysis and machine learning code as part of the active learning pipeline tightly integrated with the annotation tool. 

## Web-Based Annotation Tool Setup
This section provides guidance for setting up docker-based Django server and React-based client development and deployment environments for the annotation tool.

### Prerequisite
[Docker](https://www.docker.com/ "Docker") and [Docker Compose](https://docs.docker.com/compose/ "Docker Compose") need to be installed. On Windows 10 and above, native Docker may be installed and used. Otherwise, a Linux VM is needed. In addition, [Node.js](https://nodejs.org/en/) needs to be installed to use npm and webpack for client code development and deployment.

### Steps to set up and run the annotation tool
- git clone source code from this repo recursively to include the client code submodule

  ```
  git clone --recursive https://github.com/RENCI/ncdot-road-safety.git
  cd ncdot-road-safety
  ```

#### steps to set up the web server

- If an [iRODS server](https://irods.org/download/) optional middleware component is installed to manage and transfer images for local development on a personal computer on which image data cannot be accessed directly, you will need to create a file named ```local_settings.py``` in ```server/road_safety``` directory and put the sensitive iRODS server access credential information in the file. An example for ```local_settings.py``` is provided below that can be used as a template for creating the file.

  ```
  # iRODS server configuration info
  IRODS_ROOT = '/tmp'
  IRODS_ICOMMANDS_PATH = '/usr/bin'
  IRODS_HOST = 'host_name.research.org'
  IRODS_PORT = 1247
  IRODS_USER = 'irods_proxy_user_name'
  IRODS_PWD = 'irods_proxy_user_password'
  IRODS_ZONE = 'irods_zone_name'
  IRODS_RESC = 'irods_resource_name'
  ```

  In addition, change ```UID``` (default is ```1000```) and ```GID``` (default is ```1000```) in ```server/docker-compose.yml``` as needed to correspond to the uid and gid of the user on the host who is running docker containers for the tool. The default values should cover most if not all cases in a local development environment.

- If the image data can be accessed directly in a directory from the web server in a deployment environment, iRODS can be turned off by setting `USE_IRODS` environment variable to `False`. You can create an environment file named `.env.prod` which was set as `env_file` in `docker-compose-prod.yml`. An example for `.env.prod` is provided below that can be used as a template.

  ```
  DEBUG=False
  SECRET_KEY=secret_key_signature_created_to_be_used_by_django
  PGDATABASE=postgres_database_name
  PGUSER=postgres_db_user_name
  PGPASSWORD=postgres_db_user_password
  USER_ID=user_id_on_host
  GROUP_ID=group_id_on_host
  SSL_CERT_DIR=ssl_cert_directory
  ACCOUNTS_APPROVAL_REQUIRED=True
  EMAIL_HOST_USER=email_user_name_for_approving_user_account
  EMAIL_HOST_PWD=email_user_password_for_approving_user_account
  EMAIL_HOST=email_host_name
  EMAIL_PORT=587
  USE_IRODS=False
  IMAGE_ROOT=image_data_root_directory_on_the_host_to_be_mounted_on_container
  DEFAULT_FROM_EMAIL=email_user_used_for_default_from_email
  EMAIL_ADMIN_LIST=admin_email_address_1---admin_email_address_2
  IPAM_CONFIG_SUBNET=xxx.xxx.0.0/28
  ```


#### steps/commands to set up the client

- Run the following commands

  ```
  cd ncdot-road-safety-client
  npm install
  ```

- For local development with debugging turned on, run `npm run dev`; for production deployment, run `npm run production`.

- To collect built client bundle file `index_bundle.js` as static files to be served from the server, `cd` to the `server` directory first, then run `./collect.sh` script.

#### steps to bring the tool up and down

- From the ```server``` directory of the source tree, run ```./up.sh``` to build all containers for local development environment or run `./up_prod.sh` to build all containers for production or test server environment where `.env.prod` needs to be set up and loaded by docker-compose. 
- At this point you should be able to open up your browser to get to the tool home page for a local development environment: http://localhost:8000, or http://192.168.56.101:8000/ from the host if host-only adaptor is set up in VirtualBox for the Linux VM running on a windows box. For production or test server environment where SSL is enabled, you can go to https://host.server.address from your browser to access the tool. 
- From the ```server``` directory of the source tree, run ```./down.sh``` to bring down and clean up all containers. Alternatively, you can run ```docker-compose stop``` followed by ```docker-compose up``` if you want to keep the states of all containers for continuous development.


### Useful docker-compose commands to manage docker containers 
- ```docker-compose up``` --- bring up all containers
- ```docker-compose stop``` --- stop all containers
- ```docker-compose ps``` --- check status of all containers
- ```docker rm -fv $(docker ps -a -q)``` --- remove all containers
- ```docker rmi -f <image_id>``` where ```<image_id>``` is the image id output from ```docker images``` command which you want to remove. 

## Steps to run active learning pipeline

We run data processing/analysis and machine learning/inference offline, which are tightly integrated with the annotation tool, in an iterative active learning process. In order to run data processing/analysis scripts and machine learning/inference scripts, we recommend to set up a conda environment with all dependency libraries installed. We ran all scripts in a conda environment with python 3.8. Refer to [conda environment setup instructions](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) for details. Within the conda environment, tensorflow 2 with gpu support needs to be installed. For example, it may be installed by running the commands below:

```
conda install cudatoolkit
pip install tensorflow-gpu
conda install -c conda-forge cudnn
```

In addition, [numpy](https://numpy.org/), [scipy](https://www.scipy.org/scipylib/index.html), [matplotlib](https://matplotlib.org/), [pandas](https://pandas.pydata.org/), [scikit-learn](https://scikit-learn.org/stable/), [pillow](https://pillow.readthedocs.io/en/stable/), [dask](https://dask.org/) and [fastparquet](https://github.com/dask/fastparquet) are libraries used in some data processing and analysis scripts that may need to be installed. 

The following steps summarize how to run the active learning pipeline. 

- Use the annotation tool to collect user annotations for images sampled via an active learning sampling strategy. 
- Output user annotations from the server by running `docker exec dot-server python manage.py output_image_info_for_al <feature_name> metadata/user_annots.csv` where `<feature_name>` is the feature that has been annotated such as guardrail or pole, and `metadata/user_annots.csv` is the csv output file name that the command will output collected annotations to.
- Output remaining image base names by running: ```docker exec -ti dot-server python manage.py output_image_base_names metadata/remain_image_base_names.csv``` to be used for creating image uncertainty measures for the next round.
- Prepare images for active learning by running `python prepare_images_for_active_learning.py --input_file <user_annots.csv> --prior_input_file <all_user_annots_from_prior_al_round> --all_annot_file <all_user_annots.csv> --cur_round <cur_al_round_number> --feature_name <guardrail_or_pole_or_others> --root_dir <root_dir_to_create_al_data> --exist_train_yes_file <existing_positive_train_data_to_add_to_al> --exist_train_no_file <existing_negative_train_data_to_add_to_al>` from `machine-learning` subdirectory. Note there are some other parameters that can be set from the command line with a different value from the default. Refer to the help comment for each supported parameter in the code for details. For example, `--is_unbalanced` can be passed from the command line when the script prepares the data for active learning without taking actions to balance the data, e.g., undersample majority class to balance with minority class instances.
- Optionally run ```python create_class_weights.py``` for the data directory created by the step above if ```is_unbalanced``` flag is on which will output class weights for the unbalanced training data to be used when computing the loss in the model training by giving minority class instances more weight than the majority class instances.
- Run active learning to refine model from `machine-learning` directory by running ```nohup python active_learning.py --train_dir <train_data_dir> --val_dir <validation_data_dir> --test_dir <holdout_test_data_dir> --model_file <input_base_model_to_further_train> --output_model_file <output_model_file> --class_weights {0: 0.59, 1:3.12} &``` where class_weights dictionary is passed to fit() function for unbalanced training data. For balanced data, class_weights can be passed as `{0: 1, 1: 1}` to give both classes same weight. There are several additional parameters such as `num_of_epoch`, `batch_size`, `make_inference_only`, and `fine_tune_all_weights` which can be overridden from the command line as well. Refer to the help comment for other supported parameters in the code for details. Note that early stopping callback is used in active learning model training and only the best model with smallest loss is saved at the end of each epoch, so use the saved best model if early stopping takes effect. Also run ` python compute_model_classification_report.py` to create classification report of the best saved model on the balanced holdout test set as needed if early stopping takes effect. 
- Run split model ```python split_model_into_feature_and_head.py``` while overriding default parameters as needed for fast inference on whole active learning sample pool with common feature extraction backbone fixed.
- Run fast model prediction from feature vectors ```nohup python model_predict_features.py``` while overriding default parameters as needed.
- Evaluate model performance and create image uncertainty scores using active learning sampling strategies. For example, run `data_processing/create_uncertainty_scores.py` while overriding default parameters as needed to create uncertainty scores based on uncertainty sampling. For unbalanced data sampling such as active learning sampling for guardrail feature, similarity based sampling strategy in the feature embedding space can be used by running  ```data_processing/compute_centroid_of_features.py``` to create updated centroid of training data with the new current round annotation train data included, then running `data_processing/create_similiarity_scores.py` to create similarity scores, then running `data_processing/analyze_similarity_and_prediction.py` to analyze relationships between similarity scores and model predictions and create uncertainty measures and groups. 
- Load uncertainty scores in the annotation tool database by running ` docker exec dot-server python manage.py load_uncertainty_measures metadata/image_uncertainty_scores_round1.csv guardrail` followed by running `docker exec dot-server python manage.py create_uncertainty_groups guardrail 500` to create uncertainty groups for speeding up uncertainty measure based image queries.
- Load the latest model predictions into the annotation tool for diagnostic visualization and analysis by running  ```docker exec dot-server python manage.py update_ml_predict <prediction_csv_file>```.

Running the steps below gets the annotation tool ready for another round of active learning.
