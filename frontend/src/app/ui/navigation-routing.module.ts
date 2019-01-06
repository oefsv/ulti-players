import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminClubListComponent } from './admin/admin-club-list/admin-club-list.component';
import { AdminNewClubComponent } from './admin/admin-new-club/admin-new-club.component';
import { ClubAddMembershipComponent } from './club-add-membership/club-add-membership.component';
import { ClubListComponent } from './club-list/club-list.component';
import { ClubManageComponent } from './club-manage/club-manage.component';
import { NavigationComponent } from './navigation.component';
import { StartComponent } from './start/start.component';
import { UserComponent } from './user/user.component';

const routes: Routes = [
  {
    path: '',
    component: NavigationComponent,
    // component: StartComponent,
    // canActivate: [AuthGuard],
    children: [
      { path: '', component: StartComponent, pathMatch: 'full' },
      { path: 'clubs', component: ClubListComponent },
      { path: 'clubs/:id', component: ClubManageComponent },
      { path: 'clubs/:id/add', component: ClubAddMembershipComponent },
      { path: 'user', component: UserComponent },
      {
        path: 'rest-test',
        loadChildren: 'src/app/ui/rest-test/rest-test.module#RestTestModule'
      },
      {
        path: 'admin/clubs',
        component: AdminClubListComponent,
        pathMatch: 'full'
      },
      { path: 'admin/clubs/new', component: AdminNewClubComponent },
      { path: 'admin/club/:id', component: AdminNewClubComponent }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NavigationRoutingModule {}

export const routedComponents = [
  NavigationComponent,
  UserComponent,
  StartComponent,
  AdminClubListComponent,
  AdminNewClubComponent
];
