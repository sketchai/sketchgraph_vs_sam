# Convert SketchGraphs to SAM

This package allows to convert SktechGraphs data model to SAM.

## Installation


We use conda as an environment manager and poetry as dependency manager.

1. Generate a conda env 

First, create and activate a basic conda env from the [env_prep.yml](./env/env.yml) file. 

Run 
```
    conda env create -f ./env/env.yml
```

then 

```
    conda activate env_prep
```

NB: it can be good to change the conda name env into [env_basic_conda.yml](./env/env_basic_conda.yml) file.


2. Install poetry and package dependencies

To install package dependencies with poetry, 

```
    poetry install
```

To update package dependencies, 
```
    poetry update
```


## Testing 

For running all the tests:

```
    poetry run pytest 
```

For running a specific test: 
```
    poetry run pytest path/my_test
```


See test coverage : [TO COMPLETE]