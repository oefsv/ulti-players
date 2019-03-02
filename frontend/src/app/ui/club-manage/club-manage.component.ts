import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ClubService } from '../../models/services/club.service';
import { NavigationBarService } from './../navigation-bar.service';

@Component({
  selector: 'frisbee-club-manage',
  templateUrl: './club-manage.component.html',
  styleUrls: ['./club-manage.component.scss']
})
export class ClubManageComponent implements OnInit, OnDestroy {

  clubId: any;

  constructor(private readonly _route: ActivatedRoute,
              private readonly clubService: ClubService,
              private readonly navigationBarService: NavigationBarService) { }

  ngOnInit(): void {
    this.clubId = this._route.snapshot.params.id;

    if (this.clubId !== undefined) {
      this.clubService.getClub(this.clubId).subscribe(club => {
        this.navigationBarService.setTitle(`Verein » ${club.name}`);
      });
    }
    this.navigationBarService.setTitle('Verein');
  }

  ngOnDestroy(): void {
    // this.paramsSubscription.unsubscribe();
  }

}
