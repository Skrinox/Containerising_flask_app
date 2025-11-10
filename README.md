# CI-with-github

run the code:

    pip install -r reauirements.txt
    python app.py

the app runs on http://127.0.0.1:5000

test the app:

python -m unittest 

# Build and run with docker

`docker build --tag flask-app .`

`docker run -p 5000:5000 flask-app`