# Python Localstack Examples


Create new virtual envionment to run examples against 
localstack docker venv. Execution of your code can be 
done in docker as well.

```
$ cd localstack_service

$ docker-compose build --no-cache 

$ docker-compose up --scale dask-worker=4
```

# Dask Notes

**Dask dashboard Url**: http://localhost:8787/status

**Dask client Url**   : http://localhost:8786

When working with Dask the worker package versions should match with your 
client. Where client is your code that invokes your dask workers via the scheduler. In the examples shown 
client packages are stored in requirements.txt while dask packages 
are in conda environment.yml file

Python version is set to **3.8.3** in condo environment.yml. You may change
this if you wish to match with your client version or change your client version.