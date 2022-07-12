# Learn Raft

[WIP] Distributed gRPC driven KV store written in python for learning Raft

[//]: # ()
[//]: # (# Python Project Template)

[//]: # ()
[//]: # (A low dependency and really simple to start project template for Python Projects.)

[//]: # ()
[//]: # (See also )

[//]: # (- [Flask-Project-Template]&#40;https://github.com/rochacbruno/flask-project-template/&#41; for a full feature Flask project including database, API, admin interface, etc.)

[//]: # (- [FastAPI-Project-Template]&#40;https://github.com/rochacbruno/fastapi-project-template/&#41; The base to start an openapi project featuring: SQLModel, Typer, FastAPI, JWT Token Auth, Interactive Shell, Management Commands.)

[//]: # ()
[//]: # (### HOW TO USE THIS TEMPLATE)

[//]: # ()
[//]: # (> **DO NOT FORK** this is meant to be used from **[Use this template]&#40;https://github.com/rochacbruno/python-project-template/generate&#41;** feature.)

[//]: # ()
[//]: # (1. Click on **[Use this template]&#40;https://github.com/rochacbruno/python-project-template/generate&#41;**)

[//]: # (3. Give a name to your project  )

[//]: # (   &#40;e.g. `my_awesome_project` recommendation is to use all lowercase and underscores separation for repo names.&#41;)

[//]: # (3. Wait until the first run of CI finishes  )

[//]: # (   &#40;Github Actions will process the template and commit to your new repo&#41;)

[//]: # (4. If you want [codecov]&#40;https://about.codecov.io/sign-up/&#41; Reports and Automatic Release to [PyPI]&#40;https://pypi.org&#41;  )

[//]: # (  On the new repository `settings->secrets` add your `PIPY_API_TOKEN` and `CODECOV_TOKEN` &#40;get the tokens on respective websites&#41;)

[//]: # (4. Read the file [CONTRIBUTING.md]&#40;CONTRIBUTING.md&#41;)

[//]: # (5. Then clone your new project and happy coding!)

[//]: # ()
[//]: # (> **NOTE**: **WAIT** until first CI run on github actions before cloning your new project.)

[//]: # ()
[//]: # (### What is included on this template?)

[//]: # ()
[//]: # (- 🖼️ Templates for starting multiple application types:)

[//]: # (  * **Basic low dependency** Python program &#40;default&#41; [use this template]&#40;https://github.com/rochacbruno/python-project-template/generate&#41;)

[//]: # (  * **Flask** with database, admin interface, restapi and authentication [use this template]&#40;https://github.com/rochacbruno/flask-project-template/generate&#41;.)

[//]: # (  **or Run `make init` after cloning to generate a new project based on a template.**)

[//]: # (- 📦 A basic [setup.py]&#40;setup.py&#41; file to provide installation, packaging and distribution for your project.  )

[//]: # (  Template uses setuptools because it's the de-facto standard for Python packages, you can run `make switch-to-poetry` later if you want.)

[//]: # (- 🤖 A [Makefile]&#40;Makefile&#41; with the most useful commands to install, test, lint, format and release your project.)

[//]: # (- 📃 Documentation structure using [mkdocs]&#40;http://www.mkdocs.org&#41;)

[//]: # (- 💬 Auto generation of change log using **gitchangelog** to keep a HISTORY.md file automatically based on your commit history on every release.)

[//]: # (- 🐋 A simple [Containerfile]&#40;Containerfile&#41; to build a container image for your project.  )

[//]: # (  `Containerfile` is a more open standard for building container images than Dockerfile, you can use buildah or docker with this file.)

[//]: # (- 🧪 Testing structure using [pytest]&#40;https://docs.pytest.org/en/latest/&#41;)

[//]: # (- ✅ Code linting using [flake8]&#40;https://flake8.pycqa.org/en/latest/&#41;)

[//]: # (- 📊 Code coverage reports using [codecov]&#40;https://about.codecov.io/sign-up/&#41;)

[//]: # (- 🛳️ Automatic release to [PyPI]&#40;https://pypi.org&#41; using [twine]&#40;https://twine.readthedocs.io/en/latest/&#41; and github actions.)

[//]: # (- 🎯 Entry points to execute your program using `python -m <learn_raft>` or `$ learn_raft` with basic CLI argument parsing.)

[//]: # (- 🔄 Continuous integration using [Github Actions]&#40;.github/workflows/&#41; with jobs to lint, test and release your project on Linux, Mac and Windows environments.)

[//]: # ()
[//]: # (> Curious about architectural decisions on this template? read [ABOUT_THIS_TEMPLATE.md]&#40;ABOUT_THIS_TEMPLATE.md&#41;  )

[//]: # (> If you want to contribute to this template please open an [issue]&#40;https://github.com/rochacbruno/python-project-template/issues&#41; or fork and send a PULL REQUEST.)

[//]: # ()
[//]: # ([❤️ Sponsor this project]&#40;https://github.com/sponsors/arunma/&#41;)

[//]: # ()
[//]: # (<!--  DELETE THE LINES ABOVE THIS AND WRITE YOUR PROJECT README BELOW -->)

[//]: # ()
[//]: # (---)

[//]: # (# learn_raft)

[//]: # ()
[//]: # ([![codecov]&#40;https://codecov.io/gh/arunma/learn_raft/branch/main/graph/badge.svg?token=learn_raft_token_here&#41;]&#40;https://codecov.io/gh/arunma/learn_raft&#41;)

[//]: # ([![CI]&#40;https://github.com/arunma/learn_raft/actions/workflows/main.yml/badge.svg&#41;]&#40;https://github.com/arunma/learn_raft/actions/workflows/main.yml&#41;)

[//]: # ()
[//]: # (Distributed gRPC driven KV store written in python for learning Raft)

[//]: # ()
[//]: # (## Install it from PyPI)

[//]: # ()
[//]: # (```bash)

[//]: # (pip install learn_raft)

[//]: # (```)

[//]: # ()
[//]: # (## Usage)

[//]: # ()
[//]: # (```py)

[//]: # (from learn_raft import BaseClass)

[//]: # (from learn_raft import base_function)

[//]: # ()
[//]: # (BaseClass&#40;&#41;.base_method&#40;&#41;)

[//]: # (base_function&#40;&#41;)

[//]: # (```)

[//]: # ()
[//]: # (```bash)

[//]: # ($ python -m learn_raft)

[//]: # (#or)

[//]: # ($ learn_raft)

[//]: # (```)

[//]: # ()
[//]: # (## Development)

[//]: # ()
[//]: # (Read the [CONTRIBUTING.md]&#40;CONTRIBUTING.md&#41; file.)

[//]: # ()


Notes: 

```
pip install --editable .
learn_raft start-all
learn_raft client request_vote "Arun"  
learn_raft client get "Arun"  

``` 
