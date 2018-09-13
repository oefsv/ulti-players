import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Association } from '../models/association.model';

@Injectable()
export class RegionalAssociationService {
  constructor() { }

  getRegionalAssociations(): Observable<Association> {
    return of(
      { id: 1, name: 'St. LV' },
      { id: 2, name: 'Wien. LV' },
      { id: 3, name: 'OÖLVFS' }
    );
  }
}
