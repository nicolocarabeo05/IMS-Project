#!/usr/bin/env sh
# docker pull ghcr.io/arclabssoftware/demo-hris:main
# docker compose -f docker-compose.yml stop hris worker beat redis
# docker compose -f docker-compose.yml rm -f hris worker beat redis
# docker compose -f docker-compose.yml up -d hris worker beat redis
# docker compose -f docker-compose.yml run --rm hris migrate

# dangling_images=$(docker images -f "dangling=true" -q)
# if [ -n "$dangling_images" ]; then
#   docker rmi $dangling_images
# fi

#!/usr/bin/env sh
set -e  # Stop if any command fails

docker pull ghcr.io/nicolocarabeo05/IMS-Project:main

# Stop and remove only the existing services
docker compose -f docker-compose.yml stop ims redis
docker compose -f docker-compose.yml rm -f ims redis

# Start the containers again
docker compose -f docker-compose.yml up -d ims redis

# Run migrations inside the live ims container
docker compose -f docker-compose.yml exec ims python manage.py migrate --noinput

# Optional: collect static files
# docker compose -f docker-compose.yml exec ims python manage.py collectstatic --noinput

# Clean up old images
dangling_images=$(docker images -f "dangling=true" -q)
if [ -n "$dangling_images" ]; then
  docker rmi $dangling_images
fi
