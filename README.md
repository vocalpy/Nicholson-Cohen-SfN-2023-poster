# Nicholson-Cohen-SfN-2023-poster

🚧 Under construction 🚧

## Set-up

### Pre-requisites

You will need:

1. git for version control

(you can install git from [Github](https://help.github.com/en/github/getting-started-with-github/set-up-git),
with your operating system package manager, or using conda.)

2. nox for running tasks

This project uses the library [nox](https://nox.thea.codes/en/stable/)
as a [task runner](https://scikit-hep.org/developer/tasks),
to automate tasks like setting up a virtual environment.
Each task is represented as what nox calls a "session",
and you can run a session by invoking nox
at the command-line with the name of the session, 
e.g. `nox -s setup` will run the session called "setup". 
We suggest using [pipx](https://github.com/pypa/pipx)
to install nox in its own isolated environment,
so that nox can be accessed system-wide without affecting
anything else on your machine.

To install nox this way:

  1. Install pipx, e.g. with the package manager [brew](https://github.com/pypa/pipx#on-macos)
(note that [brew works on Linux too](https://docs.brew.sh/Homebrew-on-Linux)).

  2. Install nox with pipx: `pipx install nox`

For other ways to install nox, please see:
https://nox.thea.codes/en/stable/tutorial.html#installation

### Set up environment and install code

Experiments were run on [Pop!_OS 22.04](https://pop.system76.com/).  
It will be easiest to set up in a similar Linux environment (e.g., Ubuntu).

1. Clone this repository with git:

```
git clone git@github.com:vocalpy/Nicholson-Cohen-SfN-2023-poster.git
cd Nicholson-Cohen-SfN-2023-poster
```

2. Set up the virtual environment with the code installed into it, by running the nox session called "setup":

```nox -s setup```

After that session runs, you can activate the virtual environment it creates like so:
```console
. .venv/bin/activate
```

### Download dataset + results

3. To test whether you can replicate experiments and analysis, you'll need to download the dataset and the results

Run the nox session called "download":  

```nox -s download```

- The dataset can be found here on Zenodo: 
  https://zenodo.org/records/10098250

- The results can be in this Open Science Framework project:  
  https://osf.io/3yv8s/

## Usage

### Re-run experiments

To re-run any individual configuration file, run this command in the activated virtual environment:

```
python src/scripts/learncurve.py learncurve data/configs/NAME-OF-CONFIG.toml
```

We provide bash scripts to re-run the experiments testing the effect of window size 
and of adding smoothing terms to the loss function.
Note that these would take quite some time to run!
But they capture the logic of the experiments.
You would run these scripts in the virtual environment after activating it.
Note that if you have a machine with multiple GPUs you will want to only run one config per GPU.
This is because pytorch-lightning tries to run on multiple GPUs by default 
but does so by running multiple copies of a script in different processes, 
which breaks the logic in the loops used by vak to generate the learning curve.

```console
export CUDA_VISIBLE_DEVICES=0
bash src/scripts/runall-window-size.sh
```

```console
export CUDA_VISIBLE_DEVICES=0
bash src/scripts/runall-loss-function.sh
```

### Re-run analysis

To re-run the analysis on the downloaded results, 
or on your replication of the results,
run the following scripts to generate summary data files.

```console
python src/scripts/analysis/summary-data-window-size.py
python src/scripts/analysis/summary-data-loss-function.py
```
