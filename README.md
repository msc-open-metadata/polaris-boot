# polaris-boot

This infrastructure repository was developed at ITU as part of a the Master thesis: _OpenDict: An Approach to Open Management of All Metadata Objects_.

**Authors**: Andreas Kongstad & Carl Bruun

**Purpose**: This repository served multiple purposes in the development of OpenDict Polaris:

1. Stores docker-compose infrastructure and utility code for builing and deploying a local Apache Polaris with the OpenDict extension.
2. Eases bootstrapping of polaris and infrastructure setup via tasks in taskfile.  
3. Contains integrations tests hitting the endpoints of a local OpenDict Polaris deployment
4. Contains sample Jupyer notebooks from OpenDict Polaris demoing and testing.

## Overview

- `polaris-spark-local` (DEPRECATED): Infrastructure for booting an instance of Apache Polaris that runs locally with spark built from source.
- `polaris-spark-local-posgres`: Infrastructure for boothing an instance of opendict polaris with a postgres backing store locally or on Azure. Jupiter notebook mounts for demoing and testing.
- `polaris-spark-minio` (DEPRECATED): There was no support for local s3.
- `tests`: Integration tests for local OpenDict Polaris deployments.
- `utils`: util scripts, e.g., for storing principle credential in evn file.
- `taskfile.yml`: collection of tasks for building, running, and bootstrapping OpenDict Polaris.

## Examples

![alt text](<assets/Screenshot 2025-06-02 at 03.31.13.png>)
![alt text](<assets/Screenshot 2025-06-02 at 03.31.49.png>)
![alt text](<assets/Screenshot 2025-06-02 at 03.33.47.png>)

## Getting started

### Prerequisuites

- A unix shell
- Docker & docker-compose
- uv
- Task
- Java version >= 22

Note: If you are on windows we make no guarentee that task/taskfile behave as intended.

- If this is the case. Go to the directories used in the tasks and execute the commands manually.

1. Install and initialize venv, init secrets,

```bash
# init commitlint and secret files
task init
```

2. Clone the polaris repository and build the docker image

```bash
git clone https://github.com/msc-open-metadata/polaris.git ..

task build:polaris-local

# Apache Polaris is built using Gradle with Java 21+ and Docker 27+
task build:polaris-opendic-postgres-admin
```

3. Run the docker-compose file. Docker required. Depending on which version you have build. Choose docker-compose task accordingly.

```bash
# Build with in-memory metastore, polaris, and jupyter/spack container.
task docker:compose:up-polaris-spark-local

# Lean build with postgres metastore and polaris
task docker:compose:up-polaris-postgres

# Heavy build with spark/jupyter notebook container.
task docker:compose:up-polaris-spark-local-postgres
```

4. Bootstrapping an engineer and hr principal. Creates the local catalog, an engineer principal, an engineer principal role, an engineer catalog role, and grants MANAGE_CATALOG priveleges to the engineer principal.

The hr principal get read only grants.

Note: You can explore the principal and other polaris entities by accessing the entities table in your postgres instance using fx, pgadmin.

```bash
task rest:bootstrap-engineer
task rest:bootstrap-hr
```

5. Open local notebook.
  The spark-jupyter container outputs a URL with a token to the local jupyter instance

- Open then local notebook. Example: curl <http://localhost:8888/>

The notebook we use to for testing the opendict implementation in polaris and the spark catalog is: `polaris-spark-local-postgres/notebooks/Iceberg - Getting Started.ipynb`

6. Running the e2e test suite:

```bash
task test
```
