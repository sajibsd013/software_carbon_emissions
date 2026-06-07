FROM node:22-alpine

RUN apk add --no-cache libc6-compat

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source
COPY . .

# Build Nuxt app (production build)
RUN npm run build

EXPOSE 3000

# Start production server
CMD ["npm", "run", "start"]