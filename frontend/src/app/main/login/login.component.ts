import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MatSnackBar, MatSnackBarRef } from '@angular/material';
import { NavigationExtras, Router } from '@angular/router';
import { AuthService } from './../../common/auth.service';

@Component({
  selector: 'frisbee-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  @ViewChild('user') userRef: ElementRef;
  @ViewChild('password') passwordRef: ElementRef;

  loading: boolean;
  errorMessage: MatSnackBarRef<any> | undefined = undefined;

  userControl = new FormControl('', [
    Validators.required /*, Validators.email*/
  ]);
  passwordControl = new FormControl('', [
    Validators.required /*, Validators.email*/
  ]);

  constructor(
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loading = false;
  }

  onLogin(): void {
    if (!this.userControl.valid || !this.passwordControl.valid) { return; }

    this.loading = true;
    if (this.errorMessage !== undefined) {
      this.errorMessage.dismiss();
    }
    this.errorMessage = undefined;

    const user = (this.userRef.nativeElement as HTMLInputElement).value;
    const password = (this.passwordRef.nativeElement as HTMLInputElement).value;

    this.authService.login(user, password).subscribe(
      () => {
        this.loading = false;

        if (this.authService.isLoggedIn()) {
          const redirect = this.authService.redirectUrl
            ? this.authService.redirectUrl
            : '/ui';

          const navigationExtras: NavigationExtras = {
            queryParamsHandling: 'preserve',
            preserveFragment: true
          };

          this.router.navigate([redirect], navigationExtras);
        }
      },
      (error: any) => {
        this.loading = false;
        this.errorMessage = this.snackBar.open('Anmeldung fehlgeschlagen!');
      }
    );
  }
}