# OU Container Builder

To run the OU Container Builder you need to install the following two requirements:

* [Python 3.8 (or higher)](https://www.python.org/downloads/)
* [Pipx](https://pipxproject.github.io/pipx/)

Then, to install the OU Container Builder run

```
pipx install https://github.com/mmh352/ou-container-builder.git
```

You can then run the OU Container Builder using the following command:

```
ou-container-builder
```

## Demo

To build the demo container:

1. Clone the repository
2. Change into the ```demo``` directory
3. Run

   ```
   ou-container-builder
   ```

The resulting container listens for connections on port 8888 and it is recommended that you mount the
```/home/ou-user``` directory as a volume.

## Development

To work on the OU Container Builder you need to install an additional dependency:

* [Poetry](https://python-poetry.org/)

Then use

```
poetry install
```

to install all Python dependencies in a project-specific virtualenv. Then start a shell that runs commands
within that virtualenv:

```
poetry shell
```

You can now run

```
ou-container-builder
```

to run your development version of the code.
