import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { Permissions } from '@frisbee-db-lib/permissions';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AuthService } from '../common/auth.service';

@Component({
  selector: 'frisbee-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
@Component({
  selector: 'frisbee-db-ui-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit {
  profilePic: string | undefined;
  isDev: boolean;
  isAdmin: boolean;

  isHandset$: Observable<boolean> = this.breakpointObserver
    .observe(Breakpoints.Handset)
    .pipe(map(result => result.matches));

  constructor(
    private breakpointObserver: BreakpointObserver,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    const hash = this.authService.getEmailHash();
    this.profilePic =
      hash !== undefined
        ? `https://www.gravatar.com/avatar/${hash}?s=32&d=mp`
        : undefined;
    this.isDev = this.authService.hasGroup(Permissions.DEV);
    this.isAdmin = this.authService.hasGroup(Permissions.ADMIN);
  }

  doLogout(): void {
    this.authService.logout();
  }
}
