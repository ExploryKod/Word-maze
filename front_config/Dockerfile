#syntax=docker/dockerfile:1
FROM node:16
WORKDIR /python-docker

RUN npm install --update npm
COPY package.json package.json
RUN npm install
COPY . .
CMD [ "nopm", "install"]
