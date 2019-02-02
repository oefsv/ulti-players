import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import {
  MatButtonModule,
  MatCardModule,
  MatIconModule,
  MatInputModule
} from '@angular/material';
import { RouterModule, Routes } from '@angular/router';
import { MissingCredentialsComponent } from './missing-credentials.component';
import { MissingCredentialsService } from './missing-credentials.service';
import { ResetPasswordStep1Component } from './reset-password-step-1/reset-password-step-1.component';
import { ResetPasswordStep2Component } from './reset-password-step-2/reset-password-step-2.component';

const routes: Routes = [
  {
    path: '',
    component: MissingCredentialsComponent
  }
];

const modules = [MatCardModule, MatIconModule, MatButtonModule, MatInputModule];

@NgModule({
  imports: [CommonModule, RouterModule.forChild(routes), ...modules],
  exports: [RouterModule, ...modules],
  declarations: [
    MissingCredentialsComponent,
    ResetPasswordStep1Component,
    ResetPasswordStep2Component
  ],
  providers: [MissingCredentialsService]
})
export class MissingCredentialsModule {}
