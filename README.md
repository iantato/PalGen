<h1>Palworld Database Generator</h1>
A CLI written in Python in-order to create a database of all the Pals and their general information that can be used for other Palworld projects.

<h2>Usage</h2>
As of the moment, you have to extract the data from the `.pak` file and extract the needed `.json` files. You can check the `constants.py` in the source code if you don't know what you need to find.
<br/><br/>
The `uv` package manager is used for managing and building the project. Thus, to use it you need to do the following:

```git
git clone https://github.com/iantato/PalGen
```

```bash
pip install uv
```

```bash
uv sync
```

```bash
uv build
```

And then to open the CLI you need to use the command:

```bash
palgen -h
```