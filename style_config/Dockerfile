#syntax=docker/dockerfile:1
FROM node:16
WORKDIR /python-docker

RUN npm install --update npm
COPY . .
RUN npm install

CMD ["/bin/bash", "-c", "cd app;npm run tailwind"]