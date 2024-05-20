#!/bin/bash
set -e

# Käynnistä Django cron-tehtävät loopissa.
while true; do
    python manage.py runcrons
    sleep 60  # Odota 60 sekuntia ennen seuraavaa suoritusta.
done
