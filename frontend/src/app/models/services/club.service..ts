import { Injectable } from '@angular/core';
import { Club } from '@frisbee-db-lib/models/club.model';
import { ClubAndTeams } from '@frisbee-db-lib/views/ClubAndTeams.model';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable()
export class ClubService {
  getClubsOfCurrentUser(): Observable<Array<Club>> {
    return of([]);
  }

  getClubsAndTeamsOfCurrentUser(): Observable<Array<ClubAndTeams>> {
    return of([]);
  }
}
