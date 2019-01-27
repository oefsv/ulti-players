# STEP 1 build static website
FROM node:alpine as builder
RUN apk update && apk add --no-cache make git
# Create app directory
WORKDIR /app
# Install app dependencies
COPY package.json package-lock.json  /app/
RUN cd /app && npm set progress=false && npm install
# Copy project files into the docker image
COPY .  /app
RUN cd /app && npm run build:prod

# STEP 2 build a small nginx image with static website
FROM nginx:alpine

## From 'builder' copy website to default nginx public folder
COPY --from=builder /app/nginx/conf/nginx.docker.conf /etc/nginx
RUN mv /etc/nginx/nginx.docker.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist/ultiplayers /usr/share/nginx/html
EXPOSE 80
