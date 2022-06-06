# Tennis-Prediction

The goal of this project is to predict the outcome of a tennis match using the data of both players.


The data used comes from https://github.com/JeffSackmann.

For the code i copy https://github.com/VincentAuriau/Tennis-Prediction (he works well)
## Linux 

```
git clone https://github.com/IIanonymeII/Tennis-Prediction.git
cd Tennis-Prediction
python -r requirement.txt

```

### Player_creation (Player_creation.py)
```
python3 Player_creation.py --year 2022

```
- `--year`: year to study (int)

It's create a Player_Profiles file in `thePlayer_year_Profiles` folder

### Match_data_creation (Match_data_creation.py)
```
python3 Match_data_creation.py --year 2022

```
- `--year`: year to study (int)

It's create a data file in `Data_year` folder


### Data_Treatment (Data_Treatment.py)
```
python3 Data_Treatment.py --year 2022

```
- `--year`: year to study (int)

It's create a indicator_dicts file in `indicators_dicts_year` folder.
It's create a reversed_indicator_dicts file in `reversed_indicators_dicts_year` folder


### Data_treatment_for_prediction (Data_treatment_for_predictio.py)
```
python3 Data_treatment_for_prediction.py --year_study 2022 --year_model 2021

```
- `--year_study`: year to study (int)
- `--year_model`: model year    (int)

It's create a data_to_be_used_final_ for use it
## windows
not available for the moment
