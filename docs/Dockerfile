FROM reg.dev.mahanova.com/registry/public/library/node:20.18.0-bookworm-slim
WORKDIR /app
COPY package.json yarn.lock tsconfig.json ./
RUN yarn install
COPY src/ ./src/
CMD ["yarn", "run", "start"]
EXPOSE 9008