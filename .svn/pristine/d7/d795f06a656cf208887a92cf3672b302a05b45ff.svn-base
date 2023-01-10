import { Injectable } from '@angular/core';
import { DataStore } from '@aws-amplify/datastore';
import { map, Observable, of, shareReplay, tap } from 'rxjs';
import { Image, Project } from 'src/models';
import { StorageService } from './storage.service';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {

  projectList: Observable<Project[]>;

  constructor(private storageService: StorageService) {
    this.projectList = new Observable(function subscribe(subscriber) {
      const subscription = DataStore.observeQuery(Project).subscribe(snapshot => {
        const { items } = snapshot;
        subscriber.next(items);
      });

      return function unsubscribe() {
        subscription.unsubscribe();
      };
    });
    this.projectList = this.projectList.pipe(shareReplay(1));
  }

  listProjects(): Observable<Project[]> {
    return this.projectList;
  }

  getProjectByID(id: string): Promise<Project | undefined> {
    return DataStore.query(Project, id);
  }

  observeProjectByID(id: string): Observable<Project | undefined> {
    const project = new Observable<Project | undefined>(function subscribe(subscriber) {
      const subscription = DataStore.observeQuery(Project, i => i.id('eq', id)).subscribe(snapshot => {
        const { items } = snapshot;
        if (items.length > 0) {
          subscriber.next(items[0] as Project);
        }
      });

      return function unsubscribe() {
        subscription.unsubscribe();
      };
    });
    return project;
  }

  observeImages(project: Project): Observable<Image[]> {
    if (!project) {
      return of([]);
    }
    return new Observable(function subscribe(subscriber) {
      const subscription = DataStore.observeQuery(Image, i => i.projectID('eq', project.id)).subscribe(snapshot => {
        const { items } = snapshot;
        subscriber.next(items);
      })

      return function unsubscribe() {
        subscription.unsubscribe();
      }
    });
  }

  observeLatestImages(project: Project): Observable<{ base64: Promise<string>, image: Image }[]> {
    const latestImages = this.observeImages(project);
    return latestImages.pipe(
      map(images => images.sort((a, b) => {
        const dateA = new Date(a.createdAt!);
        const dateB = new Date(b.createdAt!);
        return dateA.getTime() - dateB.getTime();
      })),
      map(images => images.filter(image => !image.label)),
      map(images => {
        return images.filter(image => {
          return image.imageKey
        }).map(image => {
          return {
            base64: this.storageService.getImageData('mycoins', image.imageKey!),
            image
          };
        })
      }),
      shareReplay(1)
    );
  }

  monitorImages(project: Project): Observable<{ base64: Promise<string>, image: Image }[]> {
    const latestImages = this.observeImages(project);
    return latestImages.pipe(
      map(images => images.sort((a, b) => {
        const dateA = new Date(a.createdAt!);
        const dateB = new Date(b.createdAt!);
        return dateB.getTime() - dateA.getTime();
      })),
      map(images => images.filter(image => image.label)),
      map(images => {
        return images.map(image => {
          return {
            base64: this.storageService.getImageData('mycoins', image.imageKey!),
            image
          };
        })
      }),
      shareReplay(1)
    );
  }

  async createProject(project: Project): Promise<Project> {
    return DataStore.save(
      project
    );
  }

  async deleteProject(project: Project) {
    DataStore.delete(project);
  }

  async deleteImage(image: Image) {
    DataStore.delete(image);
  }

  async updateProject(project: Project, updates: Partial<Project>) {
    await DataStore.save(Project.copyOf(project, item => {
      Object.assign(item, updates);
    }));
  }

  async updateImage(image: Image, updates: Partial<Image>) {
    await DataStore.save(Project.copyOf(image, item => {
      Object.assign(item, updates);
    }));
  }
}
