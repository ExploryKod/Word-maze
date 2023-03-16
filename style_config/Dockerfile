#syntax=docker/dockerfile:1
FROM node:16
WORKDIR /python-docker

RUN npm install --update npm
COPY . .
RUN npm install

CMD ["npx","tailwindcss","-i","./app/static/src/input.css","-o","./app/static/dist/css/output.css","--watch"]