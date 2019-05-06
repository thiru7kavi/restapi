# REST API

API to save,retrive,update,delete person details

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Python3

```
python3 --version

```

2. Activate Virtual ENV

```
virtualenv -p `which python3` isolated
source isolated/bin/activate
```

### Deploying the Stack

1. Clone this repository 

```
git clone https://github.com/thiru7kavi/restapi.git
```

2. Install Dependency:

```
pip install -r requirements.txt
```

3. Run the stack

```
python MainApp.py
```
4. Deployment :
  
If Docker daemon is available 

```
docker-compose up -d 
```
### Testing the stack

API is published to the HOST 

```
http://localhost:5000

```


