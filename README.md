# causalclub.github.io

## Local Development

```bash
npm install
python -r requirements.txt
bash scripts/render.sh
```

## Container

Docker/Podman instructions to update the website:

```bash
podman build -t causalclub .
podman run -d -v $(pwd)/www:/causalclub/www:Z causalclub
```
