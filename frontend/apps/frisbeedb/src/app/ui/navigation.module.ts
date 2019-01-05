import { LayoutModule } from '@angular/cdk/layout';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {
  MatButtonModule,
  MatCardModule,
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
  MatToolbarModule,
  MatDatepickerModule
} from '@angular/material';
import { MatSidenavModule } from '@angular/material/sidenav';
import { ClubAddMembershipComponent } from './club-add-membership/club-add-membership.component';
import { ClubListModule } from './club-list/club-list.module';
import {
  NavigationRoutingModule,
  routedComponents
} from './navigation-routing.module';
import { PlayerEditComponent } from './player-edit/player-edit.component';

@NgModule({
  imports: [
    CommonModule,
    MatGridListModule,
    MatCardModule,
    MatMenuModule,
    MatIconModule,
    MatButtonModule,
    LayoutModule,
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

    // AssociationListModule,
    ClubListModule,
    NavigationRoutingModule,
    ReactiveFormsModule,

    MatDatepickerModule
  ],
  declarations: [
    ...routedComponents,
    ClubAddMembershipComponent,
    PlayerEditComponent
  ],
  exports: [
    MatGridListModule,
    MatCardModule,
    MatMenuModule,
    MatIconModule,
    MatButtonModule,
    LayoutModule,
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
    ReactiveFormsModule,

    MatDatepickerModule

  ]
})
export class NavigationModule {}
