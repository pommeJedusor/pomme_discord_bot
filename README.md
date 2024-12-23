## Get the bot on your sever
for that you just have to follow that [link](https://discord.com/oauth2/authorize?client_id=1317513322051932270&permissions=19456&integration_type=0&scope=bot)
and choose the server you want.
don't forget you must have enough permissions inside that server

## Run the bot yourself

### Developper portal
to get the token:

`app > Bot > Reset token`

Important! set

`app > Bot > Privileged Gateway Intents > Message Content Intent > true`

otherwise it might not work properly

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
simply run it
```bash
# don't forget to change the token
docker run -d  DATABASE=db/database.db -e TOKEN=INSERT_YOUR_TOKEN_HERE -v ./data:/app/db pommejedusor/pomme_discord_bot
```
