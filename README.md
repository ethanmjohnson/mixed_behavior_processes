# Discovery and Analysis of Coordinated AI and User Behavior Online

This repository contains code for discovering and analyzing free-choice Stochastic Petri nets, as presented in our paper titled "Discovery and Analysis of Coordinated AI and User Behavior Online".

## Table of Contents

-[Introduction](#introduction)\
-[Project Structure](#project-structure)\
-[Reproducibility](#reproducibility)\
-[Usage](#usage)

## Introduction

This repository provides the implementation and analysis of free-choice Stochastic Petri nets in exploring user behaviors online. It includes tools for:

- **Generating event logs from social network data**
- **Discovery of free-choice Stochastic Petri nets**
- **Analyzing structural measures of free-choice Stochastic Petri nets**
- **Analyzing mixed online processes**

## Project Structure

The project is structured as follows:

```bash

social_network_processes/
│
├── data/                       # Folder containing the event logs and Petri net models discovered
├── calculate_centrality.py     # The 'calculate' scripts contain functions for the case studies section
├── calculate_constructs.py     
├── calculate_density.py     
├── calculate_diameter.py
├── calculate_ks_entropy.py
├── calculate_mean_waiting_time.py 
├── config.json                 # Contains the path to the project root. Update this to reflect your current path
├── free_choice_SPN.py     # Contains functions used to extend a Petri net to a free-choice Stochastic Petri net
├── generate_logs_brazil.py     # Used to generate event logs from the Brazil dataset
├── generate_logs_spain_thailand.py       # Used to generate event logs from the Spain and Thailand datasets
├── generate_logs_uae_honduras.py       # Used to generate event logs from the UAE and Honduras datasets
├── generate_petri_nets.py      # Used to discover the Petri nets from an event log
├── split_log_behaviours.py      # Used to extract the coordinated and uncoordinated behaviors from an uncoordinated Petri net
│
├── requirements.txt            # List of required Python packages
└── README.md                   # Project description and instructions  

```


## Reproducibility

To obtain the results from our paper, follow these steps.

1. Navigate to the `config.json` file and update the project root entry with the path to the `mixed_behavior_processes` folder.
2. Download the UAE and Honduras datasets (https://zenodo.org/records/10650967), Spain and Thailand datasets (https://zenodo.org/records/14189193), and Brazil datasets (https://zenodo.org/records/10669936), save these in the `social_network_processes/data` folder. 
3. Pass the UAE and Honduras datasets through `generate_logs_uae_honduras.py`. For UAE use `trim_length = 10` and `log_length = 300`. For Honduras use `trim_length = 10` and `log_length = 400` (these variables are already set depending on which dataset is passed).
4. Pass the Spain and Thailand datasets through `generate_logs_spain_thailand.py`. For Spain use `trim_length = 10` and `log_length = 3000`. For Thailand use `trim_length = 10` and `log_length = 1500` (these variables are already set).
5. Pass the Brazil dataset through `generate_logs_brazil.py`. Use `trim_length = 10` and `log_length = 200` (these variables are already set).
6. Use `generate_petri_nets.py` to discover Petri nets for each of the six event logs generated in steps 2, 3 and 4.
7. Use `calculate_centrality.py` to calculate the centrality measures of the Petri nets.
8. Use `calculate_diameter.py` to calculate the diameter of the Petri nets.
9. Use `calculate_density.py` to calculate the density of the Petri nets.
10. Use `calculate_ks_entropy.py` to calculate the KS entropy.
11. Use `calculate_mean_waiting_time.py` to generate a plot comparing the mean waiting time for uncoordinated and coordinated datasets.
12. Use `calculate_constructs.py` to calculate the number of XOR and AND gates from the discovered process trees.
13. Use `split_log_behaviours.py` to extract an event log and Petri net describing the different user behaviors from an uncoordinated Petri net.
14. Repeat steps 7-12 to calculate different metrics for these split behavior Petri nets.


## Usage

The dependencies required for running the code in this repository can be installed using

```bash
pip install -r requirements.txt

```

Each script in this repository should be run from the terminal, passing in the required argument. For example, finding the designated arguments for running `calculate_diameter.py` can be found by running

```bash
python calculate_diamter.py --help

```

This shows that the required argument is a country, so we can run the script using

```bash
python calculate_diameter.py --country honduras
```

