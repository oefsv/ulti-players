import { LayoutModule } from '@angular/cdk/layout';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {
  MatButtonModule,
  MatCardModule,
  MatDatepickerModule,
  MatFormFieldModule,
  MatGridListModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatOptionModule,
  MatPaginatorModule,
  MatProgressSpinnerModule,
  MatRadioModule,
  MatSelectModule,
  MatSortModule,
  MatTableModule
} from '@angular/material';
import { RouterModule, Routes } from '@angular/router';
import { AdminAssociationListComponent } from './admin-association-list/admin-association-list.component';
import { AdminClubListComponent } from './admin-club-list/admin-club-list.component';
import { AdminNewAssociationComponent } from './admin-new-association/admin-new-association.component';
import { AdminNewClubComponent } from './admin-new-club/admin-new-club.component';
import { AdminNewPersonComponent } from './admin-new-person/admin-new-person.component';
import { AdminNewTeamComponent } from './admin-new-team/admin-new-team.component';
import { AdminPersonListComponent } from './admin-person-list/admin-person-list.component';
import { AdminTeamListComponent } from './admin-team-list/admin-team-list.component';

const routes: Routes = [
  {
    path: 'clubs',
    component: AdminClubListComponent,
    pathMatch: 'full'
  },
  { path: 'clubs/new', component: AdminNewClubComponent },
  { path: 'club/:id', component: AdminNewClubComponent },
  {
    path: 'associations',
    component: AdminAssociationListComponent,
    pathMatch: 'full'
  },
  { path: 'associations/new', component: AdminNewAssociationComponent },
  { path: 'association/:id', component: AdminNewAssociationComponent },
  {
    path: 'teams',
    component: AdminTeamListComponent,
    pathMatch: 'full'
  },
  { path: 'teams/new', component: AdminNewTeamComponent },
  { path: 'team/:id', component: AdminNewTeamComponent },
  {
    path: 'persons',
    component: AdminPersonListComponent,
    pathMatch: 'full'
  },
  { path: 'persons/new', component: AdminNewPersonComponent },
  { path: 'person/:id', component: AdminNewPersonComponent }
];

const modules = [
  LayoutModule,
  MatIconModule,
  MatButtonModule,
  MatCardModule,
  MatListModule,
  MatRadioModule,
  MatOptionModule,
  MatSelectModule,
  MatTableModule,
  MatSortModule,
  FormsModule,
  MatFormFieldModule,
  MatInputModule,
  MatProgressSpinnerModule,
  MatGridListModule,
  ReactiveFormsModule,
  MatPaginatorModule,

  MatDatepickerModule
];

@NgModule({
  imports: [CommonModule, RouterModule.forChild(routes), ...modules],
  declarations: [
    AdminClubListComponent,
    AdminNewClubComponent,
    AdminAssociationListComponent,
    AdminNewAssociationComponent,
    AdminTeamListComponent,
    AdminNewTeamComponent,
    AdminPersonListComponent,
    AdminNewPersonComponent
  ],
  exports: [...modules]
})
export class AdminModule {}
