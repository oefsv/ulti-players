import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { PWD_RESET_1, PWD_RESET_2 } from '@frisbee-db-lib/rest-constants';

@Injectable()
export class MissingCredentialsService {
  constructor(private httpClient: HttpClient) {}

  resetPasswordStep1(email: string): void {
    const data = { email };
    this.httpClient.post<string>(PWD_RESET_1, data).subscribe(data => {
      console.log(data);
    });
  }

  resetPasswordStep2(
    uid: string,
    token: string,
    password1: string,
    password2: string
  ): void {
    const data = {
      uid,
      token,
      new_password1: password1,
      new_password2: password2
    };
    this.httpClient.post<string>(PWD_RESET_2, data).subscribe(data => {
      console.log(data);
    });
  }
}
