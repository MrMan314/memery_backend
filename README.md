# Backend of The Memery

## Setup

1. Create a new python virtual environment, run `python3 -m venv venv`
2. Activate the virtual environment, run `. venv/bin/activate`
3. Install the requirements, run `pip install -r requirements.txt`
4. Run uwsgi: `uwsgi --http 127.0.0.1:5000 --master -p 4 -w wsgi:`

Please view the [main repo](https://www.github.com/MrMan314/memery) for further instructions on setting up the frontend.
