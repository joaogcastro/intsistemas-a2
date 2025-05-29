
#!/bin/bash
docker build --no-cache -t python-api .
docker run -p 5000:5000 --name python-api --network host python-api