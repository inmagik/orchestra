#!/bin/bash

source ../env/bin/activate
celery -A backend  worker -l info
