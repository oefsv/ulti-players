import { ClubManageComponent } from './club-manage/club-manage.component';
import { ClubListModule } from './club-list/club-list.module';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClubListComponent } from './club-list/club-list.component';
import { NavigationComponent } from './navigation.component';
import { UserComponent } from './user/user.component';

const routes: Routes = [
  {
    path: '',
    component: NavigationComponent,
    // canActivate: [AuthGuard],
    children: [
      { path: 'clubs', component: ClubListComponent },
      { path: 'clubs/:id', component: ClubManageComponent },
      { path: 'user', component: UserComponent },
      {
        path: 'rest-test',
        loadChildren:
          'apps/frisbeedb/src/app/ui/rest-test/rest-test.module#RestTestModule'
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NavigationRoutingModule {}

export const routedComponents = [NavigationComponent, UserComponent];
