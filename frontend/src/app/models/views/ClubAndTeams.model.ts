import { Team } from '../models/team.model';
import { Club } from '../models/club.model';

export interface ClubAndTeams {
  club: Club;
  teams?: Array<Team>;
}
