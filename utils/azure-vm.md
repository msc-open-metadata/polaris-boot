# Steps

## Create free credit VM

- Add JIT/SSH access.

## Access machine and clone repositories

### 1. Install java

```bash
sudo apt update
java -version
```

```bash
sudo apt install default-jdk
```

Set the JAVA_HOME variable

```bash
sudo update-alternatives --config java
```

```bash
sudo vim /etc/environment
```

Set JAVA_HOME

```bash
JAVA_HOME="/usr/lib/jvm/java-21-openjdk-arm64"
```

Reload env

```bash
source /etc/environment
```

Test

```bash
echo $JAVA_HOME
```

### 2. Install docker:

Uninstall conflicting packages

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

```bash
docker --version
```

### Setting up the repositories

```bash
mkdir opendict
cd opendict
git clone ...
git clone ...
cd polaris-boot
```

Install UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Running OpenDict Polaris

Install Task

```bash
sudo snap install task --classic
# Set completions
eval "$(task --completion bash)"
```

```bash
sudo task build:opendic:sudo-polaris-postgres-admin
```

```bash
task docker:sudo-polaris-jdbc
```

```bash
## For local
task rest:bootstrap-engineer

## For azure
task rest:azure-catalog:bootstrap-engineer
```

```bash
task test
```

### Setup nginx

**Domain using https://www.duckdns.org/domains**
DOMAIN: opendict.duckdns.org

```bash
sudo apt update
sudo apt install -y certbot curl git
```

Get certs with docker

```bash
docker run -v "/etc/letsencrypt:/etc/letsencrypt" -v "/var/log/letsencrypt:/var/log/letsencrypt" infinityofspace/certbot_dns_duckdns:latest \
   certonly \
     --non-interactive \
     --agree-tos \
     --email <your-email> \
     --preferred-challenges dns \
     --authenticator dns-duckdns \
     --dns-duckdns-token <your-duckdns-token> \
     --dns-duckdns-propagation-seconds 60 \
     -d "example.duckdns.org"

#Successfully received certificate.
#Certificate is saved at: /etc/letsencrypt/live/opendict.duckdns.org/fullchain.pem
#Key is saved at:         /etc/letsencrypt/live/opendict.duckdns.org/privkey.pem
```

Edit or create a config file

```bash
sudo vim /etc/nginx/sites-available/https-8181

server {
    listen 443 ssl;
    server_name opendict.duckdns.org;

    ssl_certificate     /etc/letsencrypt/live/opendict.duckdns.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/opendict.duckdns.org/privkey.pem;

    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:8181;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then link and reload:

```bash
sudo ln -s /etc/nginx/sites-available/https-8181 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Debugging

Container logs

```bash
sudo docker logs polaris-postgres-1
sudo docker logs polaris-admin-tool
sudo docker logs polaris
```

Remove containers

```bash
# Stop all running containers (if any)
sudo docker stop $(sudo docker ps -q)

# Remove all containers
sudo docker rm $(sudo docker ps -aq)
```

Get ip

```bash
docker exec <container> sh -c "curl -s https://ifconfig.me"
```

### Standard use setups

```bash
task build:opendic:sudo-polaris-postgres-admin
```

```bash
task docker:sudo-polaris-jdbc
```

```bash
task rest:bootstrap-engineer-linux
task rest:azure-catalog:bootstrap-engineer-linux
```

```bash
task test
```
