// const FORMAT_JSON_FULL = '/?format=json';

export const AUTH_LOGIN = '/api/rest/login/';
export const AUTH_LOGOUT = '/api/rest/logout/';
export const AUTH_USER = '/api/rest/user/';

export const PWD_RESET_1 = '/api/rest/password/reset/';
export const PWD_RESET_2 = '/api/rest/password/reset/confirm/';
export const PWD_CHANGE = '/api/rest/password/change/';

export const URL_GROUPS = '/api/iam/groups/';
export const URL_CLUBS = '/api/player_management/clubs/';
export const URL_CLUB_ID = '/api/player_management/club/';
export const getClubUrl = (clubId: string | number): string =>
  `/api/player_management/club/${clubId}/`;

export const URL_ASSOCIATIONS = '/api/player_management/associations/';
export const URL_ASSOCIATION_ID = '/api/pm/association/';
export const getAssociationUrl = (associationId: string | number): string =>
  `/api/player_management/association/${associationId}/`;

export const URL_TEAMS = '/api/player_management/teams/';
export const URL_TEAM_ID = '/api/player_management/team/';
export const getTeamUrl = (teamId: string | number): string =>
  `/api/player_management/team/${teamId}/`;

export const URL_PERSONS = '/api/player_management/persons/';
export const URL_PERSON_ID = '/api/player_management/person/';
export const getPersonUrl = (personId: string | number): string =>
  `/api/player_management/person/${personId}/`;
