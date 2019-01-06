import { Id } from './id.model';

export interface NewOrganisation {
  name: string;
  description?: string;
  founded_on: string;
  dissolved_on?: string;
}
export interface Organisation extends NewOrganisation, Id {}
