import { Id } from './id.model';
import { NewOrganisation, Organisation } from './organisation.model';

// tslint:disable-next-line:no-empty-interface
export interface NewClub extends NewOrganisation {}

// tslint:disable-next-line:no-empty-interface
export interface Club extends NewClub, Id {}
