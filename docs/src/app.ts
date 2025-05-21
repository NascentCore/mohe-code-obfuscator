import './types/fastify';
import fastify from 'fastify';
import { createConnection } from 'typeorm';
import documentRoutes from './routes/documents';
import { Document } from './entities/Document';
import { config } from './config';

async function main() {
    // 创建数据库连接
    await createConnection({
        type: 'postgres',
        host: config.db.host,
        port: config.db.port,
        username: config.db.username,
        password: config.db.password,
        database: config.db.database,
        entities: [Document],
        synchronize: true // 开发环境使用，生产环境建议使用迁移
    });

    const server = fastify({
        logger: true
    });

    // 注册路由
    server.register(documentRoutes);

    // 启动服务器
    try {
        await server.listen({ 
            port: config.server.port, 
            host: config.server.host 
        });
        console.log('Server is running');
    } catch (err) {
        server.log.error(err);
        process.exit(1);
    }
}

main(); 