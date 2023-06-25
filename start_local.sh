#!/bin/bash

exec $(which gunicorn) -c /code/config/gunicorn/config.py core.asgi:application