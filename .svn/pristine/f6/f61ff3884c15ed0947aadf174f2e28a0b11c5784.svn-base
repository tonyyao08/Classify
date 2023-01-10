import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Pipe({
  name: 'safeResource'
})
export class SafeResourcePipe implements PipeTransform {

  constructor(protected sanitizer: DomSanitizer) { }

  public transform(value: any): SafeResourceUrl {
    return this.sanitizer.bypassSecurityTrustResourceUrl(value);
  }

}
