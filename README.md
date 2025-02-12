# Causal Club

## Compile the Website

### Local Development

```bash
npm install
python -r requirements.txt
bash src/scripts/render.sh
```

### Container

Docker/Podman instructions to update the website:

```bash
docker build -t causalclub .
docker run -v $(pwd)/www:/causalclub/www:Z -v $(pwd)/src:/causalclub/src:Z causalclub
```

## Deploy the Website

```bash
rsync -avz --delete --exclude ".well-known" www/ causalclub:/web/
```
