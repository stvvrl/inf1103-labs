FROM python:3.12-slim
WORKDIR /usr/src/app
COPY *.py ./
COPY inventory.json .
CMD ["python", "inventory_manager.py"]