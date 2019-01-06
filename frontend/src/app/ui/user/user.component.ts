import { Component, OnInit } from '@angular/core';
import { User } from '@frisbee-db-lib/models/user.model';
import { UserService } from '@frisbee-db-lib/user/user.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'frisbee-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss'],
  providers: [UserService]
})
export class UserComponent implements OnInit {
  $currentUser: Observable<User>;

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.$currentUser = this.userService.getCurrentUser();
  }
}
