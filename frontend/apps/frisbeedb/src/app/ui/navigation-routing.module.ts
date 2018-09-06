import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AssociationListComponent } from './association-list/association-list.component';
import { NavigationComponent } from './navigation.component';
import { UserComponent } from './user/user.component';

const routes: Routes = [
  {
    path: '',
    component: NavigationComponent,
    // canActivate: [AuthGuard],
    children: [
      { path: 'association', component: AssociationListComponent },
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
