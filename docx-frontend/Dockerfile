# ==========================================
# Multi-stage Dockerfile for DocX Frontend
# ==========================================

# Stage 1: Build the React + Vite application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency specifications
COPY package*.json ./

# Install dependencies cleanly
RUN npm ci || npm install

# Copy application source code
COPY . .

# Build production bundle to /app/dist
RUN npm run build

# Stage 2: Serve production bundle with Nginx
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
