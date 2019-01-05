export interface LoginResult {
    token: string;
    user: LoginUserResult;
    email5: string;
}

export interface LoginUserResult {
    url: string;
    email: string;
    groups: Array<string>;
    username: string;
}
export interface LoginGroupResult {
    url: string;
    name: string;
}
export type LoginGroupsResult = Array<LoginGroupResult>;
