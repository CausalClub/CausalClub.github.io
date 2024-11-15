# causalclub.github.io

Docker/Podman instructions to update the website:

```bash
podman build -t causalclub .
podman run -d -v $(pwd):/output:Z causalclub
```
