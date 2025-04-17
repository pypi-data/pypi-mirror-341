# pynetbox-api
FastAPI layer above pynetbox lib.

---

You can provide environment variables to communicate with NetBox at `./pynetbox_api/env.py` or use the API (by creating the endpoint into the sqlite database via FastAPI app routes)

## Install using pip
- Production mode using pypi package

```
pip install pynetbox-api
```

## Install using git
- Developer mode using git repository
```
git clone https://github.com/emersonfelipesp/pynetbox-api.git
cd pynetbox-api
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

## Start FastAPI app (Optional)

> **OBS:** This is optional because this lib was created with the intention to be used as a lib, where you import it into your project.
> The FastAPI is available to make it easy to test each NetBox object/model with all validation and features this project provides.

```
uv run fastapi dev
```

You can optionally pass `--host` and `--port` attributes, like:

```
uv run fastapi dev --host 0.0.0.0 --port 8800
```

This will start FastAPI listening on all host network interfaces IP addresses and HTTP port 8800.
