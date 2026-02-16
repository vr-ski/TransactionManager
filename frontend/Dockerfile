# ---------- Stage 1: Build the application ----------
FROM node:25-alpine AS builder

# Accept build argument for API URL (passed from docker-compose)
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

WORKDIR /app

# Copy dependency definitions first (for layer caching)
COPY package*.json ./
RUN npm ci

# Copy the rest of the source code
COPY . .

# Build the app (output will be in /app/dist)
RUN npm run build

# ---------- Stage 2: Serve with a lightweight static server ----------
FROM node:25-alpine

# Install a simple static server globally
RUN npm install -g serve

WORKDIR /app

# Copy built app from builder stage
COPY --from=builder /app/dist ./dist

# Expose the port (serve defaults to 3000, we'll use that)
EXPOSE 3000

# Serve the static files with SPA fallback enabled
CMD ["serve", "-s", "dist", "-l", "3000"]
