# Stage 1: Build static assets
FROM node:20-alpine as builder

WORKDIR /app

COPY src/frontend/package*.json ./
RUN npm ci

COPY src/frontend/ ./
RUN npm run build

# Stage 2: Serve using Nginx
FROM nginx:1.25-alpine

COPY --from=builder /app/dist /usr/share/nginx/html
# Copy standard custom nginx config if required, otherwise defaults work on port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
