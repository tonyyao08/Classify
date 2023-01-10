import { Component, OnDestroy, OnInit, Inject } from '@angular/core';
import { flush } from '@angular/core/testing';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { DatabaseService } from 'src/app/core/database.service';
import { Project } from 'src/models';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { DeleteProjectDialogComponent } from '../../delete-project-dialog/delete-project-dialog.component';


@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit, OnDestroy {

  id: string | null = null;
  project: Project | undefined = undefined;
  isTraining = true;
  projectSubscription?: Subscription;

  constructor(private route: ActivatedRoute, private database: DatabaseService, private router: Router,
    private dialog: MatDialog) { }

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    if (this.id) {
      this.projectSubscription = this.database.observeProjectByID(this.id).subscribe(project => {
        this.project = project;
        if (project?.isTraining === undefined || project.isTraining === null) {
          this.isTraining = false;
        } else {
          this.isTraining = project.isTraining;
        }
      });
    }
  }

  ngOnDestroy(): void {
    if (this.projectSubscription) {
      this.projectSubscription.unsubscribe();
    }
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(DeleteProjectDialogComponent, {
      width: '400px'
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result} ${result.length}`);
      if (result) {
        this.deleteProject()
      }
    });
  }

  deleteProject() {
    this.database.deleteProject(this.project!).then(() => {
      this.router.navigate(['/']);
    });
  }

  toggleTraining(event: MatSlideToggleChange) {
    const { checked } = event;
    if (this.project) {
      this.database.updateProject(this.project!, {
        isTraining: checked
      });
    }
  }

}