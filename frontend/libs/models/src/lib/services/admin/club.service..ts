import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Club, NewClub } from '@frisbee-db-lib/models/club.model';
import { URL_CLUB_ID, URL_CLUBS } from '@frisbee-db-lib/rest-constants';
import { Observable } from 'rxjs';

@Injectable()
export class AdminClubService {
  constructor(private httpClient: HttpClient) {}

  getClubs(): Observable<Array<Club>> {
    return this.httpClient.get<Array<Club>>(URL_CLUBS);
  }

  getClub(clubId: string): Observable<Club> {
    return this.httpClient.get<Club>(URL_CLUB_ID + clubId);
  }

  createClub(newClub: NewClub): Observable<string> {
    return this.httpClient.post<string>(URL_CLUBS, newClub);
  }
}
