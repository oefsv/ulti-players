import { AuthService } from './../../common/auth.service';
import { Component, OnInit } from '@angular/core';
import { NavigationExtras, Router } from '@angular/router';

@Component({
  selector: 'frisbee-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  constructor(private authService: AuthService, private router: Router) {}

  loading: boolean;

  ngOnInit() {
    this.loading = false;
  }

  onLogin() {
    this.loading = true;

    this.authService.login().subscribe(() => {
      this.loading = false;

      if (this.authService.isLoggedIn) {
        // Get the redirect URL from our auth service
        // If no redirect has been set, use the default
        const redirect = this.authService.redirectUrl
          ? this.authService.redirectUrl
          : '/ui/association';

        // Set our navigation extras object
        // that passes on our global query params and fragment
        const navigationExtras: NavigationExtras = {
          queryParamsHandling: 'preserve',
          preserveFragment: true
        };

        // Redirect the user
        this.router.navigate([redirect], navigationExtras);
      }
    });
  }
}
