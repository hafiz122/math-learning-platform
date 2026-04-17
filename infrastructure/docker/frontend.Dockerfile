FROM node:20-alpine AS build

ARG VITE_API_BASE_URL=http://localhost:8000
WORKDIR /app

COPY apps/frontend/package*.json ./
RUN npm install

COPY apps/frontend/ ./
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

FROM nginx:1.27-alpine
COPY infrastructure/docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
