import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { NewTeam, Team } from '@frisbee-db-lib/models/team.model';
import { getTeamUrl } from '@frisbee-db-lib/rest-constants';
import { Observable } from 'rxjs';
import { URL_TEAMS } from '../../rest-constants';

@Injectable()
export class AdminTeamService {
  constructor(private httpClient: HttpClient) {}

  getTeams(): Observable<Array<Team>> {
    return this.httpClient.get<Array<Team>>(URL_TEAMS);
  }

  getTeam(teamId: string): Observable<Team> {
    return this.httpClient.get<Team>(getTeamUrl(teamId));
  }

  createTeam(newTeam: NewTeam): Observable<Team> {
    return this.httpClient.post<Team>(URL_TEAMS, newTeam);
  }

  editTeam(team: Team): Observable<Team> {
    return this.httpClient.put<Team>(getTeamUrl(team.id), team);
  }

  deleteTeam(team: Team): Observable<void> {
    return this.httpClient.delete<void>(getTeamUrl(team.id));
  }
}
