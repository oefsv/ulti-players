import { MissingCredentialsService } from './../missing-credentials.service';
import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'pm-reset-password-step-2',
  templateUrl: './reset-password-step-2.component.html',
  styleUrls: ['./reset-password-step-2.component.scss']
})
export class ResetPasswordStep2Component {
  @ViewChild('uidfield') uidField: ElementRef;
  @ViewChild('tokenfield') tokenField: ElementRef;
  @ViewChild('password1field') password1Field: ElementRef;
  @ViewChild('password2field') password2Field: ElementRef;

  constructor(private credentialsService: MissingCredentialsService) {}

  onClick(): void {
    const uid = (this.uidField.nativeElement as HTMLInputElement).value;
    const token = (this.tokenField.nativeElement as HTMLInputElement).value;
    const password1 = (this.password1Field.nativeElement as HTMLInputElement)
      .value;
    const password2 = (this.password2Field.nativeElement as HTMLInputElement)
      .value;
    if (uid.length > 0) {
      this.credentialsService.resetPasswordStep2(
        uid,
        token,
        password1,
        password2
      );
    }
  }
}
