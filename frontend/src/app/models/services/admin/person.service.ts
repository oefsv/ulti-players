import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { NewPerson, Person } from '@frisbee-db-lib/models/person.model';
import { getPersonUrl, URL_PERSONS } from '@frisbee-db-lib/rest-constants';
import { Observable } from 'rxjs';

@Injectable()
export class AdminPersonService {
  constructor(private readonly httpClient: HttpClient) {}

  getPersons(): Observable<Array<Person>> {
    return this.httpClient.get<Array<Person>>(URL_PERSONS);
  }

  getPerson(personId: string): Observable<Person> {
    return this.httpClient.get<Person>(getPersonUrl(personId));
  }

  createPerson(newPerson: NewPerson): Observable<Person> {
    return this.httpClient.post<Person>(URL_PERSONS, newPerson);
  }

  editPerson(person: Person): Observable<Person> {
    return this.httpClient.put<Person>(getPersonUrl(person.id), person);
  }

  deletePerson(person: Person): Observable<void> {
    return this.httpClient.delete<void>(getPersonUrl(person.id));
  }
}
