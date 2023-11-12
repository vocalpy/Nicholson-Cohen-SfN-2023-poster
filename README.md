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

We provide bash scripts to re-run the experiments testing the effect of window size and of 

### Re-run analysis
