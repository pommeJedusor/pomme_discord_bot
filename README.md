## Set-Up

### Dev
copy the .env.ini file and rename it .env
```bash
cp .env.ini .env
```

then change the TOKEN value in it by your discord bot token
```python
# .env
TOKEN=INSERT_TOKEN # put your discord bot's token here
```

then create a virtual env and install the dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

then you can run it
```bash
python3 main.py
```


### Docker
with docker you can either build the image or pull it,
if you choose to pull it you don't even need to clone this github repo

#### make the image
```bash
# build the image
docker build -t pomme_discord_bot .
# don't forget to change the token
docker run -d -e DATABASE=db/database.db -e TOKEN=INSERT_YOUR_TOKEN_HERE -v ./data:/app/db pomme_discord_bot
```

#### pull the image
then create a volume and run it
```bash
# pull the image from the docker hub
docker pull pommejedusor/pomme_discord_bot
# don't forget to change the token
docker run -d  DATABASE=db/database.db -e TOKEN=INSERT_YOUR_TOKEN_HERE -v ./data:/app/db pommejedusor/pomme_discord_bot
```
