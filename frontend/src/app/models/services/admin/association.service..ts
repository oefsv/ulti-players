import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {
  Association,
  NewAssociation
} from '@frisbee-db-lib/models/association.model';
import { getAssociationUrl, URL_CLUBS } from '@frisbee-db-lib/rest-constants';
import { Observable } from 'rxjs';
import { URL_ASSOCIATIONS } from './../../rest-constants';

@Injectable()
export class AdminAssociationService {
  constructor(private httpClient: HttpClient) {}

  getAssociations(): Observable<Array<Association>> {
    return this.httpClient.get<Array<Association>>(URL_ASSOCIATIONS);
  }

  getAssociation(associationId: string): Observable<Association> {
    return this.httpClient.get<Association>(getAssociationUrl(associationId));
  }

  createAssociation(newAssociation: NewAssociation): Observable<Association> {
    return this.httpClient.post<Association>(URL_ASSOCIATIONS, newAssociation);
  }

  editAssociation(association: Association): Observable<Association> {
    return this.httpClient.put<Association>(
      getAssociationUrl(association.id),
      association
    );
  }

  deleteAssociation(association: Association): Observable<void> {
    return this.httpClient.delete<void>(getAssociationUrl(association.id));
  }
}
