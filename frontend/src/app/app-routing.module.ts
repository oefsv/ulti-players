import { LayoutModule } from '@angular/cdk/layout';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import {
  MAT_SNACK_BAR_DEFAULT_OPTIONS,
  MatButtonModule,
  MatCardModule,
  MatDividerModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatProgressSpinnerModule,
  MatSnackBarModule
} from '@angular/material';
import { MAT_DATE_LOCALE, MatNativeDateModule } from '@angular/material/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './common/auth-guard.service';
import { AuthService } from './common/auth.service';
import { LoginComponent } from './main/login/login.component';
import { PageNotFoundComponent } from './main/page-not-found/page-not-found.component';

const routes: Routes = [
  {
    path: 'ui',
    loadChildren: 'src/app/ui/navigation.module#NavigationModule'
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
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFTOKEN'
    }),
    MatNativeDateModule,

    MatCardModule,
    MatIconModule,
    MatButtonModule,
    LayoutModule,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
    ReactiveFormsModule,
    MatDividerModule,
    MatSnackBarModule
  ],
  providers: [
    AuthGuard,
    AuthService,
    { provide: MAT_DATE_LOCALE, useValue: 'de-DE' },
    { provide: MAT_SNACK_BAR_DEFAULT_OPTIONS, useValue: { duration: 2500 } }
  ],
  exports: [
    RouterModule,
    MatNativeDateModule,
    MatCardModule,
    MatIconModule,
    MatButtonModule,
    LayoutModule,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
    ReactiveFormsModule,
    MatDividerModule,
    MatSnackBarModule
  ]
})
export class NameRoutingModule {}
