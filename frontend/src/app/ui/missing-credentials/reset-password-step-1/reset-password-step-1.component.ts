import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MissingCredentialsService } from './../missing-credentials.service';

@Component({
  selector: 'pm-reset-password-step-1',
  templateUrl: './reset-password-step-1.component.html',
  styleUrls: ['./reset-password-step-1.component.scss']
})
export class ResetPasswordStep1Component {
  @ViewChild('emailfield') emailField: ElementRef;

  controlForm = this.fb.group({
    email: [undefined, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private credentialsService: MissingCredentialsService
  ) {}

  onClick(): void {
    if (this.controlForm.valid) {
      const email = this.controlForm.get('email').value;
      this.credentialsService.resetPasswordStep1(email);
    }
  }
}
