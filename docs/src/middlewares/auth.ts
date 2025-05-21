import { FastifyRequest, FastifyReply } from 'fastify';
import { config } from '../config';
import { UsersClient } from '../clients/users';
import { AuthorizationNotProvided, AuthorizationInvalid, UsersServiceNotAvailable } from '../exceptions';

export async function getUserId(request: FastifyRequest): Promise<string> {
    const userId = request.headers[config.userIdHeader.toLowerCase()] as string;
    if (userId) {
        return userId;
    }

    const authorization = request.headers.authorization;
    if (!authorization) {
        throw new AuthorizationNotProvided();
    }

    const usersService = new UsersClient(authorization);
    return await usersService.getUserId();
}

export async function authMiddleware(
    request: FastifyRequest,
    reply: FastifyReply
) {
    try {
        const userId = await getUserId(request);
        request.userId = userId;
    } catch (error) {
        if (error instanceof AuthorizationNotProvided) {
            reply.code(401).send({ error: 'Authorization required' });
            return;
        }
        if (error instanceof AuthorizationInvalid) {
            reply.code(401).send({ error: 'Authorization invalid' });
            return;
        }
        if (error instanceof UsersServiceNotAvailable) {
            reply.code(503).send({ error: 'Users service not available' });
            return;
        }
        reply.code(500).send({ error: 'Internal server error' });
    }
} 