# SnakeBITE

A user-friendly Shiny GUI developed in python for customize and launch modular genomics data analysis pipelines using Snakemake, from Nanopore Oxford Technologies data.

## Installation

### 0. Prerequisites

- [Conda](https://docs.conda.io/en/latest/miniconda.html) is required to be installed on your system for basic program use.
- [Git](https://git-scm.com/) is required to be installed on your system for cloning the repository.
- [Dorado](https://github.com/nanoporetech/dorado) (Due to licensing restrictions, please download and install Dorado separately)

### 1a. Clone the repository

To download this software, you can clone this repository on your local system, inside your current directory (from now on called ```/path/to/SnakeBITE```) by executing the following commands:

```sh
git clone https://github.com/Lab-CoMBINE/SnakeBITE.git
cd SnakeBITE
```

### 2. Main conda environment Installation

From ```/path/to/SnakeBITE```, please make sure to create and activate the main conda environment:

```sh
conda env create -f environment.yaml
conda activate snkbt_snakemake_env
```

### 3. Individual tools conda environment installation

From ```/path/to/SnakeBITE```, please set up each conda environment with the featured data analysis tools that you do not already have:

#### Create longshot conda environment
```sh
conda env create -f envs/snkbt_longshotenv.yaml
```

#### Create Nanocaller and Clair3 conda environment
```sh
conda env create -f envs/snkbt_nanoclair3env.yaml
```

#### Create sniffles conda environment
```sh
conda env create -f envs/snkbt_sniffles2env.yaml
```

#### Create svim and cutesv conda environment
```sh
conda env create -f envs/snkbt_svimcutesvenv.yaml
```

#### Create vep conda environment
```sh
conda env create -f envs/snkbt_vepenv.yaml
```

### 4. Specific dependencies Installation

Make sure to install extra requirements from the provided file:

```sh
pip install -r requirements.txt
```

## Usage

### Shiny GUI Launch

Launch SnakeBITE GUI using the following command line:

```sh
shiny run --reload path/to/SnakeBITE/app/app.py
```

Congratulations: you are inside SnakeBITE now. Follow the instructions in the web browser page to build your own modular pipeline on ONT data.

## Project Structure

Brief schematic of the project:

```
SnakeBITE/
├── app/
│   ├── app.py                          # Main shiny application
│   ├── server_launch.py                # Pipeline launcher script
│   ├── server_utils.py                 # Utility functions for the Shiny server side
│   ├── ui_pipelines.py                 # Script for pipeline definition on Shiny ui side
│   ├── ui_toolparameters.py            # Script for parameter configuration on Shiny ui side
│   ├── ui_utils.py                     # Utility functions for the Shiny ui side
│   ├── filexplorer_ssh.py              # Script for appearance and explore ssh and sftp server
│   ├── compiler.py                     # Snakemake command compiler script
├── config.yaml                         # Main Snakemake config.yaml file
├── environment.yaml                    # Main conda environment
├── requirements.txt                    # Extra pip dependencies
├── workflow/   
    ├── envs/   
    │   ├── snkbt_longshotenv.yaml      # conda env for longshot tool
    │   ├── snkbt_nanoclair3env.yaml    # conda env for Nanocaller and Clair3 tools
    │   ├── snkbt_sniffles2env.yaml     # conda env for sniffles tool
    │   ├── snkbt_svimcutesvenv.yaml    # conda env for svim and cutesv tools
    │   ├── snkbt_vepenv.yaml           # conda env for vep tool
    ├── scripts.py                      # Snakemake python helper functions
    ├── Snakefile                       # Snakemake workflow definition
```

## Contribution
If you want to contribute to this repository, please follow these steps:
1.   Fork this repository
2.   Create a branch              -> git checkout -b feature/ProposedFeature
3.   Commit your modifications    -> git commit -m 'Add some ProposedFeature'
4.   Push your branch             -> git push origin feature/ProposedFeature
5.   Open a pull request

## License
This project is licensed under the GNU General Public License v3.0 (GNU GPLv3). See the LICENSE file for details.

### Included Tools and Their Licenses
- Snakemake - MIT License
- Shiny for Python - MIT License
- Dorado - Public License Version 1.0 (requires separate download)
- minimap2 - MIT License
- samtools - MIT/Expat License
- SVIM - GNU GPL v3
- Sniffles2 - MIT License
- cuteSV - MIT License
- Gasoline - MIT License
- Longshot - MIT License
- NanoCaller - MIT License
- Clair3 - Copyright 2021 The University of Hong Kong
- DeepVariant - MIT License
- annotSV - GNU GPL v3
- VEP - Apache v2 License