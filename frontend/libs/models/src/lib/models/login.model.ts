export interface LoginResult {
    token: string;
    user: LoginUserResult;
}

export interface LoginUserResult {
    email: string;
    groups: Array<string>;
    username: string;
}
