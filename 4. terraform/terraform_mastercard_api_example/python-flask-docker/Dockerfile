FROM python:3.11-alpine
LABEL maintainer="connorli0@outlook.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["src/app.py"]
EXPOSE 8080