# EIS1600 Tools

* [File Preparation](#file-preparation)
* [Processing Workflow](#processing-workflow)
* [Installation](#installation)
  * [Common Error Messages](#common-error-messages)
* [Set Up](#set-up-virtual-environment-and-install-the-eis1600-pkg-there)
* [Working Directory Structure](#structure-of-the-working-directory)
* [Usage](#usage)
  * [convert_mARkdown_to_EIS1600TMP](#convert-markdown-to-eis1600-files)
  * [ids_insert_or_update](#eis1600TMP-to-eis1600)
  * [check_formatting](#check-eis1600-formatting)
  * [reannotation](#reannotation)
  * [q_tags_to_bio](#get-training-data-from-q-annotations)
  * [miu_random_revision](#miu-revision)

## File Preparation

1. Convert from mARkdown to EIS1600TMP with `convert_mARkdown_to_EIS1600`
2. Check the `.EIS1600TMP` and correct tagged structure
3. Mark file as ready in the Google Spreadsheet (this includes the file into our processing pipeline)
4. Optional: Run `ids_insert_or_update` on the checked `.EIS1600TMP` (or run `incorporate_newly_prepared_files_in_corpus` which will add IDs for all files listed as ready or double-checked).

If you need to change the tagged structure in an `.EIS1600` file, you do those changes with _Simple Markdown_.
Run `ids_insert_or_update` to convert the changes in _Simple Markdown_ to _EIS1600 mARkdown_.
Check the format of the EIS1600 file with `check_formatting <path/to/file>`.

## Processing Workflow

1. Run `incorporate_newly_prepared_files_in_corpus`. This script downloads the Google Sheet and processes all ready and double-checked files:
   1. Ready files are converted from EIS1600TMP to EIS1600 and IDs are added;
   2. Formatting of ready files (now EIS1600 files) and double-checked files is checked;
   3. IDs are updated if necessary.

Files are now finalized and ready to be processed by the pipeline.

2. Run `analyse_all_on_cluster`. This script analysis all files prepared by the previous step:
   1. Each file is disassembled into MIUs;
   2. Analysis routine is run for each MIU;
   3. Results are returned as a JSON for each file that contains the annotated text, the populated yml and the analysis results (as df).

The JSON files are ready to be imported into our database.

## Installation

You can either do the complete local setup and have everything installed on your machine.
Alternatively, you can also use the docker image which can execute all the commands from the EIS1600-pkg.

### Docker Installation

Install Docker Desktop: [https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/)

It should install Docker Engine as well, which can be used through command line interface (CLI).

To run a script from the EIS1600-pkg with docker, give the command to docker through CLI:
```shell
$ docker run <--gpus all> -it -v "</path/to/EIS1600>:/EIS1600" eis1600-pkg <EIS1600-pkg-command and its params>
```

Explanation:
* `docker run` starts the image, `-it` propagates CLI input to the image.
* `--gpus all`, optional to run docker with GPUs.
* `-v` will virtualize a directory from your system in the docker image.
* `-v` virtualized `</path/to/EIS1600>` from your system to `/EIS1600` in the docker image. You give the absolute path to our `EIS1600` parent directory on your machine. Make sure to replace `</path/to/EIS1600>` with the correct path on your machine! This is the part in front of the colon, after the colon the destination inside the docker image is specified (this one is fixed).
* `eis1600-pkg` the repository name on docker hub from where the image will be downloaded
* Last, the command from the package you want to execute including all parameters required by that command.

E.G., to run `q_tags_to_bio` for toponym descriptions through docker:
```shell
$ docker run -it -v "</path/to/EIS1600>:/EIS1600" eis1600-pkg q_tags_to_bio Topo_Data/MIUs/ TOPONYM_DESCRIPTION_DETECTION/toponym_description_training_data TOPD
```

To run the annotation pipeline:
```shell
$ docker run --gpus all -it -v "</path/to/EIS1600>:/EIS1600" eis1600-pkg analyse_all_on_cluster
```
Maybe add `-D` as parameter to `analyse_all_on_cluster` because parallel processing does not work with GPU.


### Local Setup

After creating and activating the eis16000_env (see [Set Up](#set-up-virtual-environment-and-install-the-eis1600-pkg-there)), use:
```shell
$ pip install eis1600
```

In case you have an older version installed, use:
```shell
$ pip install --upgrade eis1600
```

The package comes with different options, to install camel-tools use the following command.
Check also their installation instructions because atm they require additional packages [https://camel-tools.readthedocs.io/en/latest/getting_started.html#installation](https://camel-tools.readthedocs.io/en/latest/getting_started.html#installation)
```shell
$ pip install 'eis1600[NER]'
```

If you want to run the annotation pipeline, you also need to download camel-tools data:
```shell
$ camel_data -i disambig-mle-calima-msa-r13
```

To run the annotation pipeline with GPU, use this command:

```shell
$ pip install 'eis1600[EIS]'
```

**Note**. You can use `pip freeze` to check the versions of all installed packages, including `eis1600`.

### Common Error Messages

You need to download all the models ONE BY ONE from Google Drive.
Something breaks if you try to download the whole folder, and you get this error:
```shell
OSError: Error no file named pytorch_model.bin, tf_model.h5, model.ckpt.index or flax_model.msgpack found in directory EIS1600_Pretrained_Models/camelbert-ca-finetuned
```
Better to sync `EIS1600_Pretrained_Models` with our nextcloud.

If you want to install `eis1600-pkg` from source you have to add the data modules for `gazetteers` and `helper` manually.
You can find the modules in our nextcloud.

## Set Up Virtual Environment and Install the EIS1600 PKG there

To not mess with other python installations, we recommend installing the package in a virual environment.
To create a new virtual environment with python, run:
```shell
python3 -m venv eis1600_env
```

**NB:** while creating your new virtual environment, you must use Python 3.7 or 3.8, as these are version required by CAMeL-Tools.

After creation of the environment it can be activated by:
```shell
source eis1600_env/bin/activate
```

The environment is now activated and the eis1600 package can be installed into that environment with pip:
```shell
$ pip install eis1600
```
This command installs all dependencies as well, so you should see lots of other libraries being installed. If you do not, you must have used a wrong version of Python while creating your virtual environment.

You can now use the commands listed in this README.

To use the environment, you have to activate it for **every session**, by:
```shell
source eis1600_env/bin/activate
```
After successful activation, your user has the pre-text `(eis1600_env)`.

Probably, you want to create an alias for the source command in your *alias* file by adding the following line:
```shell
alias eis="source eis1600_env/bin/activate"
```

Alias files:

- on Linux:
  - `.bash_aliases`
- On Mac:
  - `.zshrc` if you use `zsh` (default in the latest versions Mac OS);

## Structure of the working directory

The working directory is always the main `EIS1600` directory which is a parent to all the different repositories.
The `EIS1600` directory has the following structure:

```
|
|---| eis_env
|---| EIS1600_JSONs
|---| EIS1600_Pretrained_Models (for annotation, sync from Nextcloud)
|---| gazetteers
|---| Master_Chronicle
|---| OpenITI_EIS1600_Texts
|---| Training_Data
```

Path variables are in the module `eis1600/helper/repo`.

## Usage

__All commands must be run from the [parent directory](#structure-of-the-working-directory) `EIS1600`!__
See also [Processing Workflow](#processing-workflow).
* Use `-D` flag to get detailed debug messages in the console.

### Annotation Pipeline

* Use `-P` flag to run annotation of MIUs in parallel, parallel processing will eat up __ALL__ resources!
* Use `-D` flag to get detailed debug messages in the console.
```shell
$ analyse_all_on_cluster
```

### Convert mARkdown to EIS1600 files

Converts mARkdown file to EIS1600TMP (without inserting UIDs).
The .EIS1600TMP file will be created next to the .mARkdown file (you can input .inProcess or .completed files as well).
This command can be run from anywhere within the text repo - use auto complete (`tab`) to get the correct path to the file.
Alternative: open command line from the folder which contains the file which shall be converted.
```shell
$ convert_mARkdown_to_EIS1600TMP <uri>.mARkdown
```

#### Batch processing of mARkdown files

Run from the [parent directory](#structure-of-the-working-directory) `EIS1600`.
Use the `-e` option to convert all files from the EIS1600 repo.
```shell
$ convert_mARkdown_to_EIS1600 -e <EIS1600_repo>
```

### EIS1600TMP to EIS1600

EIS1600TMP files do not contain IDs yet, to insert IDs run `ids_insert_or_update` on the `.EIS1600TMP` file.
Use auto complete (`tab`) to get the correct path to the file.
```shell
$ ids_insert_or_update <OpenITI_EIS1600_Text/data/path/to/file>.EIS1600TMP
```

Additionally, this routine updates IDs if you run it on a `.EIS1600` file.
Update IDs means inserting missing UIDs and updating SubIDs.
```shell
$ ids_insert_or_update <OpenITI_EIS1600_Text/data/path/to/file>.EIS1600
```

#### Batch processing

See also [Processing Workflow](#processing-workflow).
Use `incorporate_newly_prepared_files_in_corpus` to add IDs to all ready files from the Google Sheet.
```shell
$ incorporate_newly_prepared_files_in_corpus
```

### Check EIS1600 Formatting

Check if the formatting is correct (structural tagging)
```shell
$ check_formatting <OpenITI_EIS1600_Text/data/path/to/file>.EIS1600
```

#### Batch processing

Check the formatting of all `.EIS1600` files:
```shell
$ check_formatting
```
This will create a log-file with all issues found. The log file is here: `OpenITI_EIS1600_Texts/mal_formatted_texts.log`.
It will print a list of files marked as 'ready' for which no `.EIS1600TMP` file was found.
It will also print a list of files marked as 'double-cheked' for which no `.EIS1600` file was found.
Check if the author or book URI are still matching the folders and the file in the `OpenITI_EIS1600_Texts` directory.


### Reannotation

This script can be run on a folder containing files which were exported from the onine editor. Those files are MIUs but are missing directionality tags and paragraph tags (they use new lines to indicate paragraphs).
Use these flags to active the respective model for annotation:
  * NER
  * O [_Onomastics_]
  * P [_Persons and STFCOX_]
  * T [_Toponyms and BDKOPRX_]


__THIS WILL OVERWRITE THE ORIGINAL FILES IN THE FOLDER!__
```shell
$ reannotation -NER -O -P -T <path/to/folder>
```



### Get training data from Q annotations

This script can be used to transform Q-tags from EIS1600-mARkdown to BIO-labels.
The script will operate on a directory of MIUs and write a JSON file with annotated MIUs in BIO training format.
Parameters are:
1. Path to directory containing annotated MIUs;
2. Filename or path inside RESEARCH_DATA repo for JSON output file
3. BIO_main_class, optional, defaults to 'Q'. Try to use something more meaningful and distinguishable.

```shell
$ q_tags_to_bio <path/to/MIUs/> <q_training_data> <bio_main_class>
```

For toponym definitions/descriptions:
```shell
$ q_tags_to_bio Topo_Data/MIUs/ TOPONYM_DESCRIPTION_DETECTION/toponym_description_training_data TOPD
```

### MIU revision

Run the following command from the root of the MIU repo to revise automated annotated files:
```shell
$ miu_random_revisions
```

When first run, the file *file_picker.yml* is added to the root of the MIU repository.
Make sure to specify your operating system and to set your initials and the path/command to/for Kate in this YAML file.
```yaml
system: ... # options: mac, lin, win;
reviewer: eis1600researcher # change this to your name;
path_to_kate: kate # add absolute path to Kate on your machine; or a working alias (kate should already work)
```
Optional, you can specify a path from where to open files - e.g. if you only want to open training-data, set:
```yaml
miu_main_path: ./training_data/
```

When revising files, remember to change
```yaml
reviewed    : NOT REVIEWED
```
to
```yaml
reviewed    : REVIEWED
```


### TSV dump

Run the following command from the root of the MIU repo to revise create tsv files with the corpus dump:
```shell
$ tsv_dump
```

This command will create two files:
1. eis1600-structure.tsv contains all structural data from the eis1600 corpus
2. eis1600-content.tsv contains all content data from the eis1600 corpus.
   - By default, this file is splitted in 4 parts (eis1600-content_part0001.tsv, etc), so that the files are not too large. The output can be splitted in a different number of files using the argument --part, e.g. `$ tsv_dump --parts 0` will create only one file, without any parts.
   - By default, all entities will be added to the tsv output. The list of entities are: SECTIONS, TOKENS, TAGS_LISTS, NER_LABELS, LEMMAS, POS_TAGS, ROOTS, TOPONYM_LABELS, NER_TAGS, DATE_TAGS, MONTH_TAGS, ONOM_TAGS,
                        ONOMASTIC_TAGS. A different selection of output entities can be done with the argument --label_list, e.g. `$ tsv_dump --label_list NER_LABELS NER_TAGS` will output only the information included in those entities.

>  For example, to extract all TOPONYM_LABELS from the whole eis1600 data and output it to a single file, use: `$ tsv_dump --label_list TOPONYM_LABELS`
