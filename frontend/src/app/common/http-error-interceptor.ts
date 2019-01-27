import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar, MatSnackBarRef, SimpleSnackBar } from '@angular/material';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {
  private _errorRef: MatSnackBarRef<SimpleSnackBar> | undefined;

  constructor(private snackbar: MatSnackBar) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      tap((data: any) => {
        if (this._errorRef !== undefined) {
          this._errorRef.dismiss();
          this._errorRef = undefined;
        }
      }),
      catchError((error: HttpErrorResponse) => {
        this._errorRef = this.snackbar.open(
          'Fehler bei der Serveranfrage!',
          'Schließen',
          {
            duration: 20000
          }
        );

        return throwError(error);
      })
    );
  }
}
