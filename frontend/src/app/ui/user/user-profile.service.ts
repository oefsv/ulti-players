import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { PWD_CHANGE } from '@frisbee-db-lib/rest-constants';

@Injectable()
export class UserProfileService {
  constructor(private httpClient: HttpClient) {}

  changePassword(old: string, new1: string, new2: string): void {
    const data = {
      old_password: old,
      new_password1: new1,
      new_password2: new2
    };
    this.httpClient.post<string>(PWD_CHANGE, data).subscribe(data => {
      console.log(data);
    });
  }
}
