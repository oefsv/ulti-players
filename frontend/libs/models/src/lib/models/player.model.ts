import { Id } from './id.model';
import { Person } from './person.model';

export interface Player extends Id {
    number: string;
    person: Person;
}
