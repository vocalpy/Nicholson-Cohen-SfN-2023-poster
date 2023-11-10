# Nicholson-Cohen-SfN-2023-poster

🚧 Under construction 🚧

## Set-up

### Pre-requisites

These instructions use the Python tool `nox` to set up the project with a single command.
We recommend


### Set up environment and install code

Experiments were run on [Pop!_OS 22.04](https://pop.system76.com/). It will be easiest to set up in a similar Linux environment (e.g., Ubuntu).

1. Clone this repository:

```
git clone git@github.com:vocalpy/Nicholson-Cohen-SfN-2023-poster.git
cd Nicholson-Cohen-SfN-2023-poster
```

2. Set up the development environment, using `nox` results as above:

```nox -s setup```

### Download dataset + results

3. To test whether you can replicate experiments and analysis, you'll need to download the dataset and the results

3. Run `nox`

```nox -s download```

- The dataset can be found here on Zenodo:
https://zenodo.org/records/10098250

- The results can be in this Open Science Framework project:
https://osf.io/3yv8s/

## Usage

### Re-run experiments

To re-run any configuration file, run this command in the activated virtual environment:

```
python src/scripts/learncurve.py learncurve data/configs/NAME-OF-CONFIG.toml
```

### Re-run analysis
