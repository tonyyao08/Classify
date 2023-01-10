import { Component, Input, OnInit } from '@angular/core';
import { map, Observable, tap } from 'rxjs';
import { DatabaseService } from 'src/app/core/database.service';
import { Image, Project } from 'src/models';

@Component({
  selector: 'app-training',
  templateUrl: './training.component.html',
  styleUrls: ['./training.component.scss']
})
export class TrainingComponent implements OnInit {

  @Input()
  project!: Project;

  queueSize?: Observable<number>;
  latestImage?: Observable<{ base64: Promise<string>; image: Image }>;
  labels?: Observable<string[]>;

  label: string = '';
  meta: string = '';

  constructor(private database: DatabaseService) { }

  // constructor(private database: DatabaseService, private sanitizer: DomSanitizer, private fb:FormBuilder) { }

  ngOnInit(): void {
    const latestImages = this.database.observeLatestImages(this.project);
    this.latestImage = latestImages.pipe(map(images => images[0]));
    this.queueSize = latestImages.pipe(map(images => images.length));
  }

  saveImageData(image: Image) {
    if (this.label && this.meta) {
      this.database.updateImage(image, {
        label: this.label,
        rekognitionMeta: this.meta.toLowerCase().split(' ').map(meta => meta.trim()),
        userGenerated: true
      }).then(() => {
        this.label = '';
        this.meta = '';
      })
    }
  }

  deleteImage(image: Image) {
    this.database.deleteImage(image);
  }

    // Adding Meta labels
  
  // get lessons() {
  //   return this.form.controls["lessons"] as FormArray;
  // }

  // addLesson() {
  //   const lessonForm = this.fb.group({
  //     title: ['', Validators.required],
  //     level: ['beginner', Validators.required]
  //   });
  //   this.lessons.push(lessonForm);
  // }


}
