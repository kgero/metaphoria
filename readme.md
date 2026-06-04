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

## Remote server setup

The information below is for running the web app on a remote server.

### How this app is served

```
Browser → nginx → uWSGI socket → Flask (server.py)
```

nginx receives all traffic for the domain. It reads the path and forwards
`/metaphoria` requests to this app via a Unix socket. uWSGI runs the
Flask app as a persistent process, kept alive by systemd.

### Relevant files in this repo

**`metaphoria.ini`** — uWSGI config. Tells uWSGI how to run the app:
how many processes, where to put the socket, and what path to mount at.

**`server_setup.sh`** — Run once on a fresh server after cloning. It:
1. Creates a Python virtualenv and installs `requirements.txt`
2. Writes a systemd `.service` file to `/etc/systemd/system/`
3. Enables and starts the service


### First-time setup on a new server

1. Clone the github repo.
2. Download the word vector files for `/data` (they're not in the github repo; see above). 
3. Run `bash server_setup.sh`.


### Wiring to nginx

nginx config lives centrally on the server (not in this repo) because it
covers multiple apps running on the domain at once. After running `server_setup.sh`, add these
blocks to the nginx server config:

```nginx
location /metaphoria {
    include uwsgi_params;
    uwsgi_pass unix:/home/username/metaphoria/metaphoria.sock;
}
```

This should be a `.conf` file in `/etc/nginx/sites-available/`

Then reload nginx:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

[This tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04) might help.