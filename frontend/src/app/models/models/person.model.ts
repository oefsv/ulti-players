import { Id } from './id.model';

// tslint:disable-next-line:no-empty-interface
export interface NewPerson {
  sex: 'm' | 'f';
  firstname: string;
  lastname: string;
  birthdate: string;
  email?: string;
  zip?: number;
}

// tslint:disable-next-line:no-empty-interface
export interface Person extends NewPerson, Id {}
