FROM python:3.12-slim
WORKDIR /usr/src/app
COPY your_program.py .
CMD ["python", "your_program.py"]
