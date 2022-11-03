# Zebrunner python agent

Clone the repository
```sh
git clone
```


Go to repository folder
```sh
cd python_agent
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip freeze
requests
deactivate

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
cd requests
python session.py
```


