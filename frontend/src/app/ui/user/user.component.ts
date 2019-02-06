import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { User } from '@frisbee-db-lib/models/user.model';
import { UserService } from '@frisbee-db-lib/user/user.service';
import { Observable } from 'rxjs';
import { UserProfileService } from './user-profile.service';

@Component({
  selector: 'frisbee-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss'],
  providers: [UserService, UserProfileService]
})
export class UserComponent implements OnInit {
  $currentUser: Observable<User>;

  formPasswordChange: FormGroup;

  constructor(
    private userService: UserService,
    private fb: FormBuilder,
    private userProfileService: UserProfileService
  ) {
    this.formPasswordChange = this.fb.group({
      current: ['', Validators.required],
      password1: ['', Validators.required],
      password2: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.$currentUser = this.userService.getCurrentUser();
  }

  changePassword(): void {
    const current = this.formPasswordChange.get('current').value;
    const new1 = this.formPasswordChange.get('password1').value;
    const new2 = this.formPasswordChange.get('password2').value;
    this.userProfileService.changePassword(current, new1, new2);
  }
}
