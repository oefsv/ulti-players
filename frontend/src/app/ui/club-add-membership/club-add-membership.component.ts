import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'frisbee-club-add-membership',
  templateUrl: './club-add-membership.component.html',
  styleUrls: ['./club-add-membership.component.scss']
})
export class ClubAddMembershipComponent implements OnInit, OnDestroy {

  club: string;

  constructor(private _route: ActivatedRoute) { }

  ngOnInit(): void {
    this.club = this._route.snapshot.params['id'];
  }

  ngOnDestroy(): void {
    // this.paramsSubscription.unsubscribe();
  }

}
