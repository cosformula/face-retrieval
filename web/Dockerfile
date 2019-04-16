FROM node:lts-alpine as build-stage
WORKDIR /app
COPY ./package.json ./
COPY ./yarn.lock ./
COPY ./.yarnrc ./
RUN yarn
COPY . .
RUN yarn build

# production stage
FROM nginx:stable as production-stage
RUN rm /etc/nginx/conf.d/default.conf
ADD conf.d /etc/nginx/conf.d
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
