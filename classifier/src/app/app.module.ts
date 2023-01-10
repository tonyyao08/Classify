import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { AmplifyAuthenticatorModule } from '@aws-amplify/ui-angular';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { ProjectListComponent } from './project-list/project-list.component';
import { MaterialModule } from '../material.module';
import { CreateProjectDialogComponent } from './create-project-dialog/create-project-dialog.component';
import { DeleteProjectDialogComponent } from './delete-project-dialog/delete-project-dialog.component';
import { OverviewComponent } from './project/overview/overview.component';
import { TrainingComponent } from './project/training/training.component';
import { MonitoringComponent } from './project/monitoring/monitoring.component';
import { SafeResourcePipe } from './core/safe-resource.pipe';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    ProjectListComponent,
    CreateProjectDialogComponent,
    DeleteProjectDialogComponent,
    OverviewComponent,
    TrainingComponent,
    MonitoringComponent,
    SafeResourcePipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AmplifyAuthenticatorModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MaterialModule
  ],
  providers: [],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
