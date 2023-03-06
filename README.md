sudo docker run -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DATABASE=domesticus -p 5432:5432 postgres
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
