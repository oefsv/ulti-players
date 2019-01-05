import { Observable } from 'rxjs';
import { Component, OnInit } from '@angular/core';
import { ClubService } from '@frisbee-db-lib/services/club.service.';
import { Club } from '@frisbee-db-lib/models/club.model';

@Component({
  selector: 'frisbee-start',
  templateUrl: './start.component.html',
  styleUrls: ['./start.component.scss']
})
export class StartComponent implements OnInit {

  $clubs: Observable<Array<Club>>;

  constructor(private _clubService: ClubService) {}

  ngOnInit(): void {
    this.$clubs = this._clubService.getClubsOfCurrentUser();
  }

}
