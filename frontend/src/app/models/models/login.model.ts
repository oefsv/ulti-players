export interface AuthLoginResult {
  key: string;
}

export interface LoginUserResult {
  id: string;
  email: string;
  emailmd5: string;
  first_name: string;
  last_name: string;
  groups: Array<string>;
  username: string;
}

export interface AuthGroupResult {
  id: string;
  name: string;
}
export type LoginGroupsResult = Array<AuthGroupResult>;

export interface LoggedInUser {
  id: string;
  email: string;
  groups: Array<string>;
  username: string;
  first_name: string;
  last_name: string;
}
