import { HttpClient } from '@angular/common/http';
import { Injectable, isDevMode } from '@angular/core';
import { Router } from '@angular/router';
import {
  LoginGroupsResult,
  LoginResult,
  LoginUserResult
} from '@frisbee-db-lib/models/login.model';
import { Permissions } from '@frisbee-db-lib/permissions';
import { URL_GROUPS, URL_LOGIN } from '@frisbee-db-lib/rest-constants';
import { combineLatest, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

const CURRENT_GROUPS = 'fg';
const CURRENT_USER = 'fu';
const CURRENT_MAIL = 'fm';

@Injectable()
export class AuthService {
  currentUser: LoginUserResult;
  currentGroups: Array<string>;
  emailhash: string;

  redirectUrl: string;

  private _isLoggedIn = false;

  constructor(private httpClient: HttpClient, private router: Router) {}

  login(username: string, password: string): Observable<boolean> {
    const body = new URLSearchParams();
    body.set('username', username);
    body.set('password', password);

    const userObservable = this.httpClient.post<LoginResult>(
      URL_LOGIN,
      body.toString(),
      {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }
    );

    const groupsObservable = this.httpClient.get<LoginGroupsResult>(URL_GROUPS);

    return combineLatest(userObservable, groupsObservable).pipe(
      map(([userResult, groupsResult]) => {
        if (groupsResult.length === 0) {
          if (isDevMode()) {
            window.alert('No user groups defined!');
          }

          return false;
        }

        const groupUrlsToName = groupsResult.reduce((result, obj) => {
          result[obj.url] = obj.name;

          return result;
        }, {});

        this.currentGroups = [];
        userResult.user.groups.forEach((groupUrl: string) => {
          const groupName: string | undefined = groupUrlsToName[groupUrl];
          if (groupName !== undefined) {
            this.currentGroups.push(groupName);
          }
        });

        if (this.currentGroups.length === 0) {
          if (isDevMode()) {
            window.alert('Current user has no groups defined');
          }

          return false;
        }

        this.currentUser = userResult.user;
        this.emailhash = userResult.email5;
        this._isLoggedIn = true;

        this.saveLogin();

        return true;
      })
    );
  }

  isLoggedIn(): boolean {
    this.checkLogin();

    return this._isLoggedIn;
  }

  logout(): void {
    this._isLoggedIn = false;
    this.currentUser = undefined;
    this.currentGroups = undefined;
    this.clearLogin();

    this.router.navigate(['/']);
  }

  hasGroup(group: Permissions): boolean {
    this.checkLogin();

    if (!this._isLoggedIn) {
      return false;
    }

    return this.currentGroups.includes(group as string);
  }

  hasGroups(group: Array<Permissions>): boolean {
    group.forEach(element => {
      if (!this.hasGroup(element)) {
        return false;
      }
    });

    return true;
  }

  getEmailHash(): string | undefined {
    this.checkLogin();

    return this._isLoggedIn ? this.emailhash : undefined;
  }

  private clearLogin(): void {
    try {
      sessionStorage.removeItem(CURRENT_USER);
      sessionStorage.removeItem(CURRENT_GROUPS);
      sessionStorage.removeItem(CURRENT_MAIL);
    } catch (e) {}
  }

  private saveLogin(): void {
    try {
      sessionStorage.setItem(
        CURRENT_GROUPS,
        window.btoa(JSON.stringify(this.currentGroups))
      );
      sessionStorage.setItem(
        CURRENT_USER,
        window.btoa(JSON.stringify(this.currentUser))
      );
      sessionStorage.setItem(
        CURRENT_MAIL,
        window.btoa(JSON.stringify(this.emailhash))
      );
    } catch (e) {}
  }

  private checkLogin(): void {
    if (!this._isLoggedIn) {
      try {
        const groups64 = sessionStorage.getItem(CURRENT_GROUPS);
        const user64 = sessionStorage.getItem(CURRENT_USER);
        if (groups64 && user64) {
          this.currentGroups = JSON.parse(window.atob(groups64));
          this.currentUser = JSON.parse(window.atob(user64));
          this.emailhash = JSON.parse(
            window.atob(sessionStorage.getItem(CURRENT_MAIL))
          );
          this._isLoggedIn = true;
        }
      } catch (error) {
        this.currentGroups = undefined;
        this.currentUser = undefined;
        this.emailhash = undefined;
        this._isLoggedIn = false;
      }
    }
  }
}
