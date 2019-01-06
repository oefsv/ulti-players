import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Association } from '../models/association.model';

@Injectable()
export class RegionalAssociationService {

  getRegionalAssociations(): Observable<Association> {
    return of(
      { id: 1, name: 'St. LV', founded_on: '2018-01-01' },
      { id: 2, name: 'Wien. LV', founded_on: '2018-01-01' },
      { id: 3, name: 'OÖLVFS', founded_on: '2018-01-01' }
    );
  }
}
