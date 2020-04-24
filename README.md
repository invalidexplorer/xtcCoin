**Activate the virtual environment**
```
source blockchain-env/bin/activate
```

**Install all packages**
```
pip3 install -r requirements.txt
```

**Run the Tests**
Make sure to activate the virtual enviroment

```
python3 -m pytest backend/tests
```

**Run the application and the API**
Make sure to activate the virtual enviroment

```
python3 -m backend.app
```

** Run a peer instance **

Make sure to activate the virtual env.

```
export PEER=TRUE && python3 -m backend.app
```

**Run the frontend**
In the frontend directory:

```
npm run start
```