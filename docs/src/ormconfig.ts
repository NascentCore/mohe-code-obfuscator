import { config } from './config';

export default {
    type: 'postgres',
    host: config.db.host,
    port: config.db.port,
    username: config.db.username,
    password: config.db.password,
    database: config.db.database,
    entities: ["src/entities/*.ts"],
    migrations: ["migrations/*.ts"],
    cli: {
      "entitiesDir": "src/entities",
      "migrationsDir": "migrations"
    }
};