export const config = {
    userIdHeader: 'X-User-ID',
    usersBaseUrl: process.env.USERS_BASE_URL || 'http://localhost:9004',
    db: {
        host: process.env.DB_HOST || 'localhost',
        port: parseInt(process.env.DB_PORT || '5432'),
        username: process.env.DB_USER || 'postgres',
        password: process.env.DB_PASSWORD || 'postgres',
        database: process.env.DB_NAME || 'workbench-docs',
    },
    server: {
        port: parseInt(process.env.SERVER_PORT || '9008'),
        host: process.env.SERVER_HOST || '0.0.0.0',
    }
} as const; 