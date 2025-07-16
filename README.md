# Module 10: Object-Relational Mapping and Database Access
![Coverage Badge](https://github.com/lcphutchinson/is601_10/actions/workflows/ci-cd.yml/badge.svg)

A module of is601 Web Systems Development, by Keith Williams

This module introduces the SQLAlchemy ORM in conjunction with pydantic to deploy a basic user authorization scheme with bcrypt hashing.

See the Dockerhub Repo [[Here]](https://hub.docker.com/repository/docker/lcphutchinson/is601_10)

### Running the Test Suite

After cloning the repo to your local machine, create and enter virtual environment with the venv module

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, from the root folder, install the project's requirements

```bash
pip install -r requirements.txt
playwright install
```

You may be prompted by playwright to install some dependencies it needs, but its instructions are clear.
Next, deploy the docker image in daemon mode to reserve your terminal for testing.

```bash
docker compose up --build -d
```

After configuration is finished, run the test suite

```bash
pytest
```

You will find some of the redundant and ill-targetted tests have been removed or altered. I've also added some tests to accomodate my alterations to the program.
