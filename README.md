
#Install before continuing:

pip install virtualenv

virtualenv --python=" from pyenv - path to your py interpreter 3.7.0 " .venv

.venv/Scripts/activate

pip install -r requirements.txt

#Run wsgi server:

waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"

curl -v -XGET http://localhost:5000/api/v1/hello-world-6