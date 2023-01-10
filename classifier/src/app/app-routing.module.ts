import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProjectListComponent } from './project-list/project-list.component';
import { OverviewComponent } from './project/overview/overview.component';

const routes: Routes = [
  { path: 'projects', component: ProjectListComponent },
  { path: 'p/:id', component: OverviewComponent },
  { path: '', redirectTo: '/projects', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
