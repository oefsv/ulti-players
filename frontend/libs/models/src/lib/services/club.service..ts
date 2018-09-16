import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Club } from '@frisbee-db-lib/models/club.model';
import { ClubAndTeams } from '@frisbee-db-lib/views/ClubAndTeams.model';

@Injectable()
export class ClubService {
  getClubsOfCurrentUser(): Observable<Array<Club>> {
    return of([{ id: 1, name: 'Verein 1' }, { id: 2, name: 'Verein 2' }]);
  }

  getClubsAndTeamsOfCurrentUser(): Observable<Array<ClubAndTeams>> {
    return of([

      {
        club: {
          id: 1,
          name: 'Verein 0'
        }
      },
      {
        club: {
          id: 1,
          name: 'Verein 1'
        },
        teams: [
          { id: 3, name: 'Team 1.1' }
        ]
      },
      {
        club: {
          id: 2,
          name: 'Verein 2'
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
