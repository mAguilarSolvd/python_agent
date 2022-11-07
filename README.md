# Zebrunner python agent

We are using python 3.11

Clone the repository
```sh
git clone
```

Go to repository folder
```sh
cd python_agent
```


To initialize the virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip freeze
```

Build project's image and run the container
```sh
docker-compose build
docker-compose up -d
```

Enter to the api container
```sh
docker-compose exec api bash
```

Start performing requests
 ```sh
cd api
python client.py
```


