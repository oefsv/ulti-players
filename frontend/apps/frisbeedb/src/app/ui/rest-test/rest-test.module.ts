import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RestTestComponent } from './rest-test.component';
import {
  MatButtonModule,
  MatDividerModule,
  MatFormFieldModule,
  MatInputModule
} from '@angular/material';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

const routes: Routes = [
  {
    path: '',
    component: RestTestComponent
    // canActivate: [AuthGuard],
  }
];

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    HttpClientModule,
    // HttpClientXsrfModule.withOptions({
    //   cookieName: 'csrftoken'
    // }),
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatDividerModule
  ],
  exports: [],
  declarations: [RestTestComponent],
  providers: []
})
export class RestTestModule {}
