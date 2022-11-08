# tesis_codigo

```bash
conda env update -n base --file environment.yml
```
## Docker


```bash
docker run --name dslab -d \
	-p 8888:8888 -p 4040:4040 \
	-e JUPYTER_ENABLE_LAB=yes -e RESTARTABLE=yes -e GRANT_SUDO=yes \
	-e NB_UID=(id -u) -e NB_GID=(id -g) \
	--user root \
	-v "$HOME/Documents":/home/jovyan/work \
	jupyter/datascience-notebook
```