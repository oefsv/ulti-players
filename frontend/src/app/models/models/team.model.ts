import { Id } from './id.model';
import { NewOrganisation, Organisation } from './organisation.model';

// tslint:disable-next-line:no-empty-interface
export interface NewTeam extends NewOrganisation {
  club_membership?: number;
}

// tslint:disable-next-line:no-empty-interface
export interface Team extends NewTeam, Id {}
