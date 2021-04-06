# Bo.py

## Commands
- /start

> Start the bot

- /qr

> Generate a QR code from text

- /pwd

> Generates a password by taking 2 parameters
> Parameters
> 1. Alphabet
> 2. Upper case
> 3. Lower case
> 4. Numbers
> 5. Alphanumeric
> 6. Alphanumeric and Symbols
> Enter the number of your choice and/or the length, default "8".  
> For example /pwd 5 20, creates a 20 character alphanumeric password.

## Installation

### The Easy Way

#### Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/TaprisSugarbell/Bo.py)

#### The Hard Way

```sh
pipenv shell
pip install -r requirements.txt
cp sample_config.py config.py
--- EDIT config.py values appropriately ---
python index.py
```

or

```sh
pipenv shell
pipenv install -r requirements.txt
cp sample_config.py config.py
--- EDIT config.py values appropriately ---
python index.py
```

#### LICENSE
- MIT



