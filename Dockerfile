FROM python:3.5-alpine
ADD ./src /src
WORKDIR /src
RUN pip install aiohttp
CMD python app.py
