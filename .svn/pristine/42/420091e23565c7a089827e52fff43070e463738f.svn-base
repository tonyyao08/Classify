import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { Project } from 'src/models';
import { DatabaseService } from '../core/database.service';
import { CreateProjectDialogComponent } from '../create-project-dialog/create-project-dialog.component';

@Component({
  selector: 'app-project-list',
  templateUrl: './project-list.component.html',
  styleUrls: ['./project-list.component.scss']
})
export class ProjectListComponent implements OnInit {

  projects: Observable<Project[]>;

  constructor(private database: DatabaseService, public dialog: MatDialog, private router: Router) {
    this.projects = this.database.listProjects();
  }

  ngOnInit(): void {

  }

  createProject() {
    const dialogRef = this.dialog.open(CreateProjectDialogComponent, {
      width: '400px'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.length > 0) {
        this.database.createProject(new Project({
          projectName: result,
          isTraining: true
        })).then(project => {
          this.router.navigate(['/p', project.id]);
        });
      }
    });
  }

}
