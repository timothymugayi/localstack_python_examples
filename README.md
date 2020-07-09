# Python Localstack Examples


Create new virtual envionment to run examples against 
localstack docker venv. Execution of your code can be 
done in docker as well.

```
$ cd localstack_service

$ docker-compose build --no-cache 

$ docker-compose up --scale dask-worker=4
```

Dask dashboard Url: http://localhost:8787/status

Dask client Url   : http://localhost:8786