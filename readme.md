# Metaphoria

Metaphoria is a research demo based on the paper [Metaphoria: An Algorithmic Companion for Metaphor Creation](https://dl.acm.org/doi/pdf/10.1145/3290605.3300526). The code in this repository can be used to run a web app that allows you to create metaphors for a given concept.

## Setup

Runs on python3. 

### Requirements

pip install "jinja2<3.1.0"

Install requirements using requirements.txt. I recommend using a virtual environment:

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Data

Then, download the word vectors needed to run the search. Download the following zip file (~100MB to download, ~200MB once unzipped):

`https://www.dropbox.com/scl/fi/lptjoh8pyly890jvs059z/metaphoria-data.zip?dl=0`

Unzip it, and change the directory name to `/data`. You should now have the following files in your repository:

```
/data/BRM-emot-submit.csv
/data/deps.vectors.slim.txt
/data/glove.slim.txt
```

### Conceptnet

The app originally used the [ConceptNet](https://conceptnet.io/) public API, but this appears to have gone down sometime in 2025. Here was the workaround:

I downloaded the pre-built list of all edges (assertions) from the conceptnet [Github Wiki](https://github.com/commonsense/conceptnet5/wiki/Downloads); it should be called `conceptnet-assertions-5.7.0.csv.gz`. Put it in the `conceptnet` directory. Then run `extract_conceptnet.py` which slims it down to just the assertions that are relevant for Metaphoria. This should create a file named `conceptnet_en_subset.json`.

The `src/expand_source_cnet.py` file has been replaced with `cnet_local.py`, and ends up calling the .json file instead of the ConceptNet API. Since the .json file is only 8MB, I just upload it to the repo.

### Run 

To run this app from the terminal, first point flask to the correct python file:

`export FLASK_APP=server.py`

Then to run the app:

`flask run`

It takes a few seconds to load in the vectors

You can also run it in debug mode:

`flask run --debug`