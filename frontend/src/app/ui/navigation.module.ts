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
  MatMenuModule,
  MatOptionModule,
  MatPaginatorModule,
  MatProgressSpinnerModule,
  MatRadioModule,
  MatSelectModule,
  MatSortModule,
  MatTableModule,
  MatToolbarModule
} from '@angular/material';
import { MatSidenavModule } from '@angular/material/sidenav';
import { ClubAddMembershipComponent } from './club-add-membership/club-add-membership.component';
import { ClubListModule } from './club-list/club-list.module';
import {
  NavigationRoutingModule,
  routedComponents
} from './navigation-routing.module';
import { PlayerEditComponent } from './player-edit/player-edit.component';

const modules = [
  MatGridListModule,
  MatCardModule,
  MatMenuModule,
  MatIconModule,
  MatButtonModule,
  MatToolbarModule,
  MatSidenavModule,
  MatListModule,
  MatRadioModule,
  MatOptionModule,
  MatSelectModule,

  FormsModule,
  MatFormFieldModule,
  MatInputModule,
  MatProgressSpinnerModule,

  MatTableModule,
  MatPaginatorModule,
  MatSortModule,
  MatDatepickerModule,
  ReactiveFormsModule
];

@NgModule({
  imports: [
    CommonModule,

    LayoutModule,

    // AssociationListModule,
    ClubListModule,
    NavigationRoutingModule,
    ...modules
  ],
  declarations: [
    ...routedComponents,
    ClubAddMembershipComponent,
    PlayerEditComponent
  ],
  exports: [LayoutModule, ...modules]
})
export class NavigationModule {}
