import { Component, Input, OnInit } from '@angular/core';
import { map, Observable, tap } from 'rxjs';
import { DatabaseService } from 'src/app/core/database.service';
import { StorageService } from 'src/app/core/storage.service';
import { Image, Project } from 'src/models';


@Component({
  selector: 'app-monitoring',
  templateUrl: './monitoring.component.html',
  styleUrls: ['./monitoring.component.scss']
})
export class MonitoringComponent implements OnInit {

  @Input()
  project!: Project;

  latestImage?: Observable<{ base64: Promise<string>; image: Image }>;
  currImage?: Promise<string>;
  preview: Boolean = false;
  allLabels?: Observable<string[]>;
  history?: Observable<{ imageKey: string; summary: string; }[]>;

  constructor(private database: DatabaseService, private storage: StorageService) { }

  ngOnInit(): void {
    const latestImages = this.database.monitorImages(this.project);
    this.latestImage = latestImages.pipe(map(images => {
      return images[0];
    }));
    this.currImage = undefined;
    this.allLabels = latestImages.pipe(map(images => {
      return Array.from(images.map(({ image }) => image.label)
        .filter((label) => label !== null || label !== undefined)
        .map(label => label!.toUpperCase())
        .reduce((acc, curr) => {
          acc.add(curr);
          return acc;
        }, new Set<string>()));
    }));
    this.history = latestImages.pipe(
      map(images => {
        return images.map(image => {
          return {
            imageKey: image.image.imageKey!,
            summary: `${image.image.createdAt} (${image.image.label})`
          }
        })
      })
    )
  }

  getImage(event: any): void {
    this.preview = true;
    const { options } = event;
    const selected = options.find((option: any) => option.selected);
    this.currImage = this.storage.getImageData('mycoins', selected.value);
  }

}
