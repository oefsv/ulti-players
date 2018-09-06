import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { User } from '../models/user.model';

@Injectable()
export class UserService {
  constructor() {}

  getCurrentUser(): Observable<User> {
    return of({
      firstName: 'vorname',
      lastName: 'nachname',
      email: 'adresse@localhost'
    });
  }
}
