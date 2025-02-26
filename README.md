# polaris-boot

Infrastructure for booting an instance of Apache Polaris that runs locally or in S3 using Spark

## Getting started:
1. Install task
2. Clone the polaris repository and build the docker image
```bash
git clone https://github.com/msc-open-metadata/polaris.git ..

# Apache Polaris is built using Gradle with Java 21+ and Docker 27+
task docker:build:polaris-local
```

3. Clone and build the spark repository
```bash
git clone https://github.com/apache/spark.git ..
# Switch to 3.5
# git checkout branch-3.5

task docker:build:spark
```

4. Building the spark-jupyter image and running the application
```bash
task docker:build:spark-jupyter-image docker:compose:up-polaris-spark-local
```

5. Bootstrapping an engineer and hr principal:
```bash
task rest:bootstrap-engineer
task rest:bootstrap-hr
```

6. Open local notebook.
  The spark-jupyter container outputs a URL with a token to the local jupyter instance
  - Open then local notebook. Example: curl http://localhost:8888/?token=<token>


## Adding a new endpoint to Polaris:


1.Build project and generate API
```bash
./gradlew assemble
```

2.Add object and endpoint yaml specification to spec/polaris-management-service.yml

3.

Overview:
![img](./assets/rest-overview-polaris.png)
