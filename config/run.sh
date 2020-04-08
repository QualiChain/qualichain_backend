#!/usr/bin/env bash

echo " Run gunicorn"
gunicorn --workers=4 -b 0.0.0.0:5000 wsgi:app --reload