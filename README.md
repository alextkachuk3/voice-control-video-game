# Installation

```
    python -m venv ./venv
    cd venv/Scripts
    activate
    cd ../../game
    pip install -r requirements.txt
```
Also need .env file with next data:

```
API_KEY=FIREBASE_API_KEY //for online mode
AUTH_DOMAIN=FIREBASE_DOMAIN //for online mode
PROJECT_ID=FIREBASE_ID //for online mode
STORAGE_BUCKET=FIREBASE_BUCKET //for online mode
MESSAGING_SENDER_ID=FIREBASE_MESSAGING_ID //for online mode
APP_ID=FIREBASE_APP_ID //for online mode
DATABASE_URL=FIREBASE_DATABASE_URL //for online mode
OPENAI_API_KEY=OPENAI_API_KEY //for voice controllers

```

# Run

```
    cd game
    python main.py
```

# Controllers

There are two possible controllers for attacking(keyboard and voice) and only one for moving(keyboard).