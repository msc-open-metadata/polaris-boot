# polaris-boot

Infrastructure for booting an instance of Apache Polaris that runs locally or in S3 using Spark

## Prerequisuites:

1. Clone the polaris repository and build the docker image
2. Install taskfile
3. Rename example.env to local.env and fill in the variables.

## Adding a new endpoint to Polaris:


1.Build project and generate API
```bash
./gradlew assemble
```

2.Add object and endpoint yaml specification to spec/polaris-management-service.yml

3.

Overview:
![img](./assets/rest-overview-polaris.png)
