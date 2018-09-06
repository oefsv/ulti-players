import { AssociationListComponent } from './association-list.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  MatCardModule,
  MatGridListModule,
  MatIconModule,
  MatMenuModule
} from '@angular/material';

@NgModule({
  imports: [
    CommonModule,
    MatGridListModule,
    MatMenuModule,
    MatIconModule,
    MatCardModule
  ],
  declarations: [AssociationListComponent]
})
export class AssociationListModule {}
