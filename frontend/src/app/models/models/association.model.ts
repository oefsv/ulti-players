import { Id } from './id.model';
import { NewOrganisation, Organisation } from './organisation.model';

// tslint:disable-next-line:no-empty-interface
export interface NewAssociation extends NewOrganisation {}

// tslint:disable-next-line:no-empty-interface
export interface Association extends NewAssociation, Id {}
