// const FORMAT_JSON_FULL = '/?format=json';

export const URL_LOGIN = '/rest/api/auth/session/login';
export const URL_GROUPS = '/rest/iam/groups/';
export const URL_CLUBS = '/rest/pm/api/clubs/';
export const URL_CLUB_ID = '/rest/pm/club/';
export const getClubUrl = (clubId: string | number): string =>
  `/rest/pm/club/${clubId}/`;

export const URL_ASSOCIATIONS = '/rest/pm/api/associations/';
export const URL_ASSOCIATION_ID = '/rest/pm/association/';
export const getAssociationUrl = (associationId: string | number): string =>
  `/rest/pm/association/${associationId}/`;

export const URL_TEAMS = '/rest/pm/api/teams/';
export const URL_TEAM_ID = '/rest/pm/team/';
export const getTeamUrl = (teamId: string | number): string =>
  `/rest/pm/team/${teamId}/`;

export const URL_PERSONS = '/rest/pm/api/persons/';
export const URL_PERSON_ID = '/rest/pm/person/';
export const getPersonUrl = (personId: string | number): string =>
  `/rest/pm/person/${personId}/`;
