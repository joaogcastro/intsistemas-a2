#!/bin/bash
docker build --no-cache -t php-api .
docker run -p 8000:8000 --network host php-api