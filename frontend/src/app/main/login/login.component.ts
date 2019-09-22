import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar, MatSnackBarRef } from '@angular/material';
import { NavigationExtras, Router } from '@angular/router';
import { AuthService } from './../../common/auth.service';

@Component({
  selector: 'frisbee-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loading: boolean;
  errorMessage: MatSnackBarRef<any> | undefined = undefined;

  formGroup: FormGroup;

  constructor(
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.loading = false;
    this.formGroup = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onLogin(): void {
    if (!this.formGroup.valid) {
      return;
    }

    this.loading = true;
    if (this.errorMessage !== undefined) {
      this.errorMessage.dismiss();
    }
    this.errorMessage = undefined;

    const email = this.formGroup.get('email').value;
    const password = this.formGroup.get('password').value;

    this.authService.login(email, password).subscribe(
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
