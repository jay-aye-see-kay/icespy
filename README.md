# IceSpy - Inventory Management System

IceSpy is a personal web application designed to help you track meals stored in your freezer. It provides a clear, age-sorted inventory, enabling you to eat items within their ideal 3-6 month timeframe and minimize food waste.

## Setup

### Prerequisites

- devbox
- direnv

### Installation

1. install
```sh
direnv allow
uv sync
```

2. start the project
```sh
# starts django dev server on http://127.0.0.1:8000/ and start tailwind in watch mode, see ./process-compose.yaml for definition
devbox services up -b
# to view logs
tail -f .devbox/compose.log
```

3. misc tasks
```sh
# create a superuser
python manage.py createsuperuser
# make migrations (run after models have changed)
python manage.py makemigrate
# run migrations
python manage.py migrate
# build tailwind css for prod
tailwindcss -i static/css/input.css -o static/css/output.css --minify
```

