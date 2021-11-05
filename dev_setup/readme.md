# Development Environment Setup

This repo assumes a linux-based development environment. 

If none is available, consider using the [Azure Cloud Shell](https://docs.microsoft.com/en-gb/azure/cloud-shell/quickstart) or look into [https://docs.microsoft.com/en-us/windows/wsl/install](WSL).

Below, we will set up:
- Azure CLI
- Azure Functions Core Tools
- local Python environment

## Azure CLI installation and setup

If not yet available, [install the azure cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli), and confirm:

```
az version
```
use `az upgrade` if version is not > 2.2.

log in using the browser authentication flow
```
az login
```

list available subscriptions, set the working subscription and verify:
```
az account list -o table
az account set -s <subscription name>
az account show
```


## Azure Functions Core Tools installation and setup 

> Tip: see also [Work with Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)

Install the Azure functions core tools
```
npm install -g azure-functions-core-tools@3 --unsafe-perm true
```

verify v>3 is available:
```
func version
//-> 3.0.2912
```

## Python development environment

To work with python, first work from the terminal to set up a conda environment from the provided environment file, and activate it:

```
conda update conda

conda create -f py_conda_environment.yml

conda activate pyfunctions38
```
> Tip: if conda is not yet avaialble, see [here](https://gist.github.com/lindacmsheard/928b21764d0fa2c1324804de9e38953e) for a gist on setting up conda.

When running the function locally, ensure that the pyfunctions38 environment is activated in the shell, indicated by `(pyfunctions)` in front of the shell prompt.