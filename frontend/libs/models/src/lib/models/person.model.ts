import { Id } from "./id.model";

export interface Person extends Id {
    sex: 'm' | 'f';
    firstName: string;
    lastName: string;
    birthdate: string;
    email?: string;
    zip: number;
}
