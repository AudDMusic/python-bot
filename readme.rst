========================
AudD telegram bot [BETA]
========================


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: AudDBot-code-style


1) Clone repo ::

    git clone https://github.com/AudDMusic/python-bot.git
    cd python-bot

2) Copy EXAMPLE.env with your credentials ::

    cp EXAMPLE.env .env

------------------------
🐳 **Docker-deployment**
------------------------
Customize docker-compose.yml[optional] (or no)

Run docker-compose and run app services::

    docker-compose up -d

Updating::

    docker-compose build
    docker-compose restart


------------------------------------------
🐌 **Step by step for noobs (non-docker)**
------------------------------------------
Main requirement: python3.7.X ::

    python -m pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python worker.py --env .env
