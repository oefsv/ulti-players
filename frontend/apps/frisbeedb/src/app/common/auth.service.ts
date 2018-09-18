import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { LoginResult, LoginUserResult } from '@frisbee-db-lib/models/login.model';
import { RestConstants } from '@frisbee-db-lib/rest-constants';

@Injectable()
export class AuthService {
  isLoggedIn = false;
  currentUser: LoginUserResult;
  emailhash: string;

  redirectUrl: string;

  constructor(private httpClient: HttpClient, private router: Router) {}

    login(username: string, password: string): Observable<boolean> {
        const body = new URLSearchParams();
        body.set('username', username);
        body.set('password', password);

        return this.httpClient
            .post<LoginResult>(
                RestConstants.BASE + RestConstants.URL_LOGIN,
                body.toString(),
                {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
                }
            )
            .pipe(
                tap(result => {
                    this.currentUser = result.user;
                    this.emailhash = result.email5;
                    this.isLoggedIn = true;
                }),
                map(obj => true)
            );
    }

  logout(): void {
    this.isLoggedIn = false;
    this.router.navigate(['/']);
  }

  getEmailHash(): string | undefined {
      return this.isLoggedIn ? this.emailhash : undefined;
  }
}
