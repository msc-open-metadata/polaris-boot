# polaris-boot

Repository containing:
- Infrastructure for booting an instance of Apache Polaris that runs locally or in Azure using Spark
- Documentation on adding additional functionality to our polaris fork:

## Getting started:

### Prerequisuites:
- A unix shell
- Docker & docker-compose
- Task
- Java version >= 21

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

task build:build:polaris-local

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

Note: You can explore the principal and other polaris entities by accessing the entities table in your postgres instance using fx, pgadmin. (Pass)
```bash
task rest:bootstrap-engineer
task rest:bootstrap-hr
```

5. Open local notebook.
  The spark-jupyter container outputs a URL with a token to the local jupyter instance
  - Open then local notebook. Example: curl http://localhost:8888/

The notebook we use to for testing the opendict implementation in polaris and the spark catalog is: `polaris-spark-local-postgres/notebooks/Iceberg - Getting Started.ipynb`

6. Running the e2e test suite:
```
task test
```


## Changes in open-metadata/polaris

- Add spec/open-dic-service.yml
-

## Adding a new endpoint to Polaris:


1.Build project and generate API
```bash
./gradlew assemble
```

2.Add object and endpoint yaml specification to spec/polaris-management-service.yml

3.

Overview:
![img](./assets/rest-overview-polaris.png)
