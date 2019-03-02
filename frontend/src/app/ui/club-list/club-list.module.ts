import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import {
  MatButtonModule,
  MatCardModule,
  MatGridListModule,
  MatIconModule,
  MatListModule,
  MatMenuModule
} from '@angular/material';
import { RouterModule } from '@angular/router';
import { ClubService } from '@frisbee-db-lib/services/club.service';
import { ClubManageComponent } from './../club-manage/club-manage.component';
import { ClubListComponent } from './club-list.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    MatGridListModule,
    MatMenuModule,
    MatIconModule,
    MatCardModule,
    MatListModule,
    MatButtonModule
  ],
  declarations: [ClubListComponent, ClubManageComponent],
  providers: [ClubService]
})
export class ClubListModule {}
