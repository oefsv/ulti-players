import { Component, OnInit } from '@angular/core';
import { Team } from '@frisbee-db-lib/models/team.model';
import { Observable } from 'rxjs';
import { NavigationBarService } from '../navigation-bar.service';
import { Club } from './../../models/models/club.model';
import { ClubService } from './../../models/services/club.service';

@Component({
  selector: 'frisbee-start',
  templateUrl: './start.component.html',
  styleUrls: ['./start.component.scss']
})
export class StartComponent implements OnInit {
  $clubs: Observable<Array<Club>>;
  $teams: Observable<Array<Team>>;

  constructor(
    private readonly clubService: ClubService,
    private readonly navigationBarService: NavigationBarService
  ) {}

  ngOnInit(): void {
    this.navigationBarService.setTitle('Startseite');
    this.$clubs = this.clubService.getClubsOfCurrentUser();
    this.$teams = this.clubService.getTeamsOfCurrentUser();
  }
}
