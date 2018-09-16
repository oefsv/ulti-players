import { Id } from './id.model';
export interface Organisation extends Id {
    name: string;
    description?: string;
}
