import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'frisbee-club-manage',
  templateUrl: './club-manage.component.html',
  styleUrls: ['./club-manage.component.scss']
})
export class ClubManageComponent implements OnInit, OnDestroy {

  club: string;

  constructor(private _route: ActivatedRoute) { }

  ngOnInit(): void {
    this.club = this._route.snapshot.params['id'];
  }

  ngOnDestroy(): void {
    // this.paramsSubscription.unsubscribe();
  }

}
