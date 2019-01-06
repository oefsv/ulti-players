import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Club, NewClub } from '@frisbee-db-lib/models/club.model';
import { getClubUrl, URL_CLUBS } from '@frisbee-db-lib/rest-constants';
import { Observable } from 'rxjs';

@Injectable()
export class AdminClubService {
  constructor(private httpClient: HttpClient) {}

  getClubs(): Observable<Array<Club>> {
    return this.httpClient.get<Array<Club>>(URL_CLUBS);
  }

  getClub(clubId: string): Observable<Club> {
    return this.httpClient.get<Club>(getClubUrl(clubId));
  }

  createClub(newClub: NewClub): Observable<Club> {
    return this.httpClient.post<Club>(URL_CLUBS, newClub);
  }

  editClub(club: Club): Observable<Club> {
    return this.httpClient.put<Club>(getClubUrl(club.id), club);
  }

  deleteClub(club: Club): Observable<void> {
    return this.httpClient.delete<void>(getClubUrl(club.id));
  }
}
