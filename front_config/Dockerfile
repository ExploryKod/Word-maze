#syntax=docker/dockerfile:1
FROM node:16
WORKDIR /python-docker

RUN npm install --update npm
COPY . .
RUN npm install

CMD ["npx","tailwindcss","-i","./static/src/input.css","-o","./static/dist/css/output.css","--watch"]
  