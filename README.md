# What is this?

This repository contains an analysis of responses from [survey](https://unil.qualtrics.com/jfe/form/SV_bpBDplVZyRJpZ0q). The goal is to answer the question **Are people able to use theoretically effective cues to detect lies?**

# How to run the code

1. Clone the repository
2. Install the required packages
    ```bash
    pip install -r requirements.txt
    ```
3. Run the jupyter notebook
    ```bash
    jupyter notebook
    ```
4. Download the data as **TSV** from [here](https://unil.qualtrics.com/responses/#/surveys/SV_bpBDplVZyRJpZ0q). 
   Don't forget to tick **"Export viewing order data for randomized surveys"**, in the advanced options (this is done so we know which group of the cues was shown to the participant). 
5. Extract the zip file and place the `.tsv`  file in the data folder.
6. Open the notebook `analysis.ipynb` and change the `data_file` variable to be the name of the `.tsv` file in the `/data` folder.
7. Run the notebook cells.

# Contributing

Please run `nb-clea clean <notebook>` and `black .`  before committing your changes.
