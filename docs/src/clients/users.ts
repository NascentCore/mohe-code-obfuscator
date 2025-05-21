import { config } from '../config';
import { AuthorizationInvalid, UsersServiceNotAvailable } from '../exceptions';

export class UsersClient {
    constructor(private authorization: string) {}

    async getUserId(): Promise<string> {
        try {
            const response = await fetch(new URL('/v1/users/validate', config.usersBaseUrl), {
                headers: {
                    'Authorization': this.authorization
                }
            });

            if (response.status >= 500) {
                throw new UsersServiceNotAvailable();
            }

            if (response.status !== 200) {
                throw new AuthorizationInvalid();
            }

            try {
                const data = await response.json();
                if (!data.user_id) {
                    throw new AuthorizationInvalid();
                }
                return data.user_id;
            } catch (error) {
                throw new UsersServiceNotAvailable();
            }
        } catch (error) {
            if (error instanceof AuthorizationInvalid || 
                error instanceof UsersServiceNotAvailable) {
                throw error;
            }
            throw new UsersServiceNotAvailable();
        }
    }
} 