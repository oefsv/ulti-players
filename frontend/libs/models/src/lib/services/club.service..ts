import { Injectable } from '@angular/core';
import { Club } from '@frisbee-db-lib/models/club.model';
import { ClubAndTeams } from '@frisbee-db-lib/views/ClubAndTeams.model';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable()
export class ClubService {
  getClubsOfCurrentUser(): Observable<Array<Club>> {
    return of([
      { id: 1, name: 'Verein 1', founded_on: '2018-12-01' },
      { id: 2, name: 'Verein 2', founded_on: '2018-12-01' }
    ]);
  }

  getClubsAndTeamsOfCurrentUser(): Observable<Array<ClubAndTeams>> {
    return of([
      {
        club: {
          id: 1,
          name: 'Verein 0',
          founded_on: '2018-12-01'
        }
      },
      {
        club: {
          id: 4,
          name: 'Verein 1',
          founded_on: '2018-12-01'
        },
        teams: [{ id: 3, name: 'Team 1.1' }]
      },
      {
        club: {
          id: 2,
          name: 'Verein 2',
          founded_on: '2018-12-01'
        },
        teams: [
          { id: 4, name: 'Team 2.4' },
          { id: 5, name: 'Team 2.5' },
          { id: 6, name: 'Team 2.6' }
        ]
      }
    ]);
  }
}
