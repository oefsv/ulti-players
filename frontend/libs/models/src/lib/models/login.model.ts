export interface LoginResult {
    token: string;
    user: LoginUserResult;
    email5: string;
}

export interface LoginUserResult {
    email: string;
    groups: Array<string>;
    username: string;
}
