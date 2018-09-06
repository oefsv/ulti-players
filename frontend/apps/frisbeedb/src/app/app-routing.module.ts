import { LayoutModule } from '@angular/cdk/layout';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import {
  MatButtonModule,
  MatCardModule,
  MatDividerModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatProgressSpinnerModule
} from '@angular/material';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './common/auth-guard.service';
import { AuthService } from './common/auth.service';
import { LoginComponent } from './main/login/login.component';
import { PageNotFoundComponent } from './main/page-not-found/page-not-found.component';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';

const routes: Routes = [
  {
    path: 'ui',
    loadChildren: 'apps/frisbeedb/src/app/ui/navigation.module#NavigationModule'
  },
  { path: '', component: LoginComponent, pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  declarations: [LoginComponent, PageNotFoundComponent],
  imports: [
    RouterModule.forRoot(routes, {
      initialNavigation: 'enabled'
    }),
    CommonModule,
    HttpClientModule,
    // HttpClientXsrfModule.withOptions(),
    MatCardModule,
    MatIconModule,
    MatButtonModule,
    LayoutModule,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
    MatDividerModule
  ],
  providers: [AuthGuard, AuthService],
  exports: [
    RouterModule,
    MatProgressSpinnerModule,
    MatInputModule,
    MatCardModule,
    MatIconModule,
    MatDividerModule
  ]
})
export class NameRoutingModule {}
