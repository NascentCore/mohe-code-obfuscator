import 'fastify';

declare module 'fastify' {
    interface FastifyRequest {
        userId: string;
    }
}

// 确保这个文件被当作模块
export {}; 