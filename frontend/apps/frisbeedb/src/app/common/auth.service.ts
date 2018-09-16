import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { LoginResult, LoginUserResult } from '@frisbee-db-lib/models/login.model';

@Injectable()
export class AuthService {
  isLoggedIn = false;
  currentUser: LoginUserResult;

  redirectUrl: string;

  constructor(private httpClient: HttpClient, private router: Router) {}

  login(username: string, password: string): Observable<boolean> {
    return this.httpClient
      .post<LoginResult>(
        '/rest/api-token-auth-custom',
        {
          username,
          password
      }
      )
      .pipe(
        tap(result => {
          this.currentUser = result.user;
          this.isLoggedIn = true;
        }),
        map(obj => true)
      );
  }

  logout(): void {
    this.isLoggedIn = false;
    this.router.navigate(['/']);
  }
}
