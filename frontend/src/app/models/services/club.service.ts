import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Club } from '@frisbee-db-lib/models/club.model';
import { ClubAndTeams } from '@frisbee-db-lib/views/ClubAndTeams.model';
import { forkJoin, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Team } from '../models/team.model';
import { getClubUrl, URL_CLUBS, URL_TEAMS } from '../rest-constants';

@Injectable()
export class ClubService {

  constructor(private readonly httpClient: HttpClient) {}

  getClubsOfCurrentUser(): Observable<Array<Club>> {
    return this.httpClient.get<Array<Club>>(URL_CLUBS);
  }

  getTeamsOfCurrentUser(): Observable<Array<Team>> {
    return this.httpClient.get<Array<Team>>(URL_TEAMS);
  }

  getClubsAndTeamsOfCurrentUser(): Observable<Array<ClubAndTeams>> {
    const clubs$ = this.httpClient.get<Array<Club>>(URL_CLUBS);
    const teams$ = this.httpClient.get<Array<Team>>(URL_TEAMS);

    return forkJoin(clubs$, teams$)
    .pipe(map(([clubs, teams])  =>

      clubs.map(c => ({club: c}))));

  }

  getClub(clubId: string): Observable<Club> {
    return this.httpClient.get<Club>(getClubUrl(clubId));
  }

}
