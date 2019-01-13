import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
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
        path: 'admin',
        loadChildren: 'src/app/ui/admin/admin.module#AdminModule'
      }
     
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
  StartComponent
];
