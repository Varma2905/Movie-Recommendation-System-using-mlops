# Build stage for React
FROM node:18-alpine as build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
# Set API URL for production (You will provide this in Railway Variables)
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL
RUN npm run build

# Production stage using Nginx
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
# Copy nginx config template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
EXPOSE 80
# Railway provides $PORT, Nginx will use it via the template
CMD ["nginx", "-g", "daemon off;"]
