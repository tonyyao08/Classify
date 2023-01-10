import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-delete-project-dialog',
  templateUrl: './delete-project-dialog.component.html',
  styleUrls: ['./delete-project-dialog.component.scss']
})
export class DeleteProjectDialogComponent implements OnInit {

  projectName = '';

  constructor() { }

  ngOnInit(): void {
  }

}
