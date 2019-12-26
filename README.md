# BotAffinity

A simple Telegram bot to share films.

Uses a non official [API](https://github.com/dsantosmerino/filmaffinity-api).

### Usage:

- **/share** or **/film**: search a movie with the keywords provided. Shares with the group 
- **/help** show help

## Run

You need to register your bot in the [BotFather](https://telegram.me/botfather) to obtein a TOKEN

### Straight forward

```bash
pipenv shell
PYTHONPATH=$PYTHONPATH:$(pwd)/src TOKEN="YOUR_TOKEN" python src/bot_affinity/__init__.py 
```

### Docker

```bash
docker container run --rm -e TOKEN="YOUR_TOKEN" bot_affinity:latest
```

