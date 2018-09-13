import { BreakpointObserver } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { ClubService } from '@frisbee-db-lib/services/club.service.';
import { ClubAndTeams } from '@frisbee-db-lib/views/ClubAndTeams.model';
import { Observable } from 'rxjs';

@Component({
  selector: 'frisbee-club-list',
  templateUrl: './club-list.component.html',
  styleUrls: ['./club-list.component.scss'],
  providers: [ClubService]

})
export class ClubListComponent implements OnInit {

  _clubsAndTeams: Observable<Array<ClubAndTeams>>;

  constructor(private _clubService: ClubService, private breakpointObserver: BreakpointObserver) {}

  ngOnInit(): void {
    this._clubsAndTeams = this._clubService.getClubsAndTeamsOfCurrentUser();
  }

}
