export class AuthorizationNotProvided extends Error {
    constructor() {
        super('Authorization not provided');
        this.name = 'AuthorizationNotProvided';
    }
}

export class AuthorizationInvalid extends Error {
    constructor() {
        super('Authorization invalid');
        this.name = 'AuthorizationInvalid';
    }
}

export class UsersServiceNotAvailable extends Error {
    constructor() {
        super('Users service is not available');
        this.name = 'UsersServiceNotAvailable';
    }
} 