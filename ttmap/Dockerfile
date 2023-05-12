FROM node:20-alpine
WORKDIR /build
COPY . /build/
RUN npm install
RUN npm run build
# CMD ["node", "build/index.js"]
