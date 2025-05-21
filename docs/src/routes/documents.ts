import '../types/fastify';
import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { Document } from '../entities/Document';
import { getRepository,In } from 'typeorm';
import { DocumentCreateRequest, DocumentUpdateRequest, DocumentListRequest } from '../types/document';
import { authMiddleware } from '../middlewares/auth';
import { htmlToLexicalJson, lexicalJsonToHtml, lexicalJsonToMarkdown } from '../utils/transform';
import { marked } from 'marked';

export default async function (fastify: FastifyInstance) {
    const documentRepo = getRepository(Document);

    // 添加前置中间件
    fastify.addHook('preHandler', authMiddleware);

    // 获取文档列表
    fastify.get('/v1/documents', async (request: FastifyRequest<{Querystring: DocumentListRequest}>, reply: FastifyReply) => {
        const { page = 1, page_size = 10, order_by = 'created_at', order = 'desc' } = request.query;
        
        const [items, total] = await documentRepo.findAndCount({
            where: { user_id: request.userId },
            skip: (page - 1) * page_size,
            take: page_size,
            order: { [order_by]: order }
        });

        return {
            total,
            pages: Math.ceil(total / page_size),
            page,
            page_size,
            items
        };
    });

    // 创建文档
    fastify.post('/v1/documents', async (request: FastifyRequest<{Body: DocumentCreateRequest}>, reply: FastifyReply) => {
        const doc = documentRepo.create({
            ...request.body,
            user_id: request.userId
        });
        const result = await documentRepo.save(doc);
        reply.code(201);
        return result;
    });

    // 获取单个文档
    fastify.get('/v1/documents/:document_id', async (request: FastifyRequest<{Params: {document_id: string}}>, reply: FastifyReply) => {
        const doc = await documentRepo.findOne({
            where: { id: request.params.document_id, user_id: request.userId }
        });
        if (!doc) {
            reply.code(404).send({ error: 'Document not found or access denied' });
            return;
        }
        return doc;
    });

    // 更新文档
    fastify.put('/v1/documents/:document_id', async (request: FastifyRequest<{Params: {document_id: string}, Body: DocumentUpdateRequest}>, reply: FastifyReply) => {
        const doc = await documentRepo.findOne({
            where: { id: request.params.document_id, user_id: request.userId }
        });
        if (!doc) {
            reply.code(404).send({ error: 'Document not found or access denied' });
            return;
        }
        
        documentRepo.merge(doc, request.body);
        const result = await documentRepo.save(doc);
        return result;
    });

    // 删除文档
    fastify.delete('/v1/documents/:document_id', async (request: FastifyRequest<{Params: {document_id: string}}>, reply: FastifyReply) => {
        const result = await documentRepo.softDelete({
            id: request.params.document_id,
            user_id: request.userId
        });
        if (result.affected === 0) {
            reply.code(404).send({ error: 'Document not found or access denied' });
            return;
        }
        reply.code(204);
    });

    // 根据ID列表获取文档
    fastify.post('/v1/documents/details', async (request: FastifyRequest<{Body: {ids: string[]}}>, reply: FastifyReply) => {
        const { ids } = request.body;
        if (!ids || ids.length === 0) {
            reply.code(400).send({ error: 'No IDs provided' });
            return;
        }

        const documents = await documentRepo.find({
            where: {
                id: In(ids),
                user_id: request.userId
            }
        });

        return documents;
    });

    // 将文档转换为markdown或html
    fastify.get('/v1/export', async (request: FastifyRequest<{Querystring: {id: string, format: 'markdown' | 'html'}}>, reply: FastifyReply) => {
        const { id, format } = request.query;
        const doc = await documentRepo.findOne({
            where: { id, user_id: request.userId }
        });
        if (!doc) {
            reply.code(404).send({ error: 'Document not found or access denied' });
            return;
        }
        
        if (format === 'markdown') {
            return {
                id: doc.id,
                title: doc.title,
                content: lexicalJsonToMarkdown(doc.state)
            }
        } else if (format === 'html') {
            return {
                id: doc.id,
                title: doc.title,
                content: lexicalJsonToHtml(doc.state)
            }
        } else {
            reply.code(400).send({ error: 'Invalid format' });
            return;
        }
    });

    //将html转lexicalState
    fastify.post('/v1/state', async (request: FastifyRequest<{Body: {content: string,type: 'markdown' | 'html'}}>, reply: FastifyReply) => {
        const { content, type } = request.body;
        if (type === 'html') {
            return htmlToLexicalJson(content)
        } else if (type === 'markdown') {
            const html = marked(content) as string
            return htmlToLexicalJson(html)
        } else {
            reply.code(400).send({ error: 'Invalid format' });
            return;
        }
    });
} 