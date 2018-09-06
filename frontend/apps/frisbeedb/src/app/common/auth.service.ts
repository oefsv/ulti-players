import { Router } from '@angular/router';
import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';
import { delay, map, mapTo, tap } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class AuthService {
  isLoggedIn = false;

  // store the URL so we can redirect after logging in
  redirectUrl: string;

  constructor(private httpClient: HttpClient, private router: Router) {}

  login(): Observable<boolean> {
    // return this.httpClient
    //   .get(
    //     'http://venv.hbqg3zr3a3.us-west-2.elasticbeanstalk.com/api-auth/login/',
    //     {
    //       headers: {
    //         'Request-Type': 'application/json'
    //       }
    //     }
    //   )
    //   .pipe(
    //     tap(result => {
    //       console.log(result);
    //     }),
    //     map(obj => true)
    //   );
    return of(true).pipe(
      delay(1000),
      tap(val => (this.isLoggedIn = true))
    );
  }

  logout(): void {
    this.isLoggedIn = false;
    this.router.navigate(['/']);
  }
}
