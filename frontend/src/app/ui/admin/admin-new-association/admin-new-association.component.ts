import { formatDate } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material';
import { ActivatedRoute, Router } from '@angular/router';
import { Association, NewAssociation } from '@frisbee-db-lib/models/association.model';
import { AdminAssociationService } from '@frisbee-db-lib/services/admin/association.service';

@Component({
  selector: 'pm-admin-new-association',
  templateUrl: './admin-new-association.component.html',
  styleUrls: ['./admin-new-association.component.scss'],
  providers: [AdminAssociationService]
})
export class AdminNewAssociationComponent implements OnInit {
  controlForm = this.fb.group({
    name: [null, Validators.required],
    description: [null],
    founded: [null, Validators.required],
    dissolved: [null]
  });

  associationId: string | undefined;

  constructor(
    private fb: FormBuilder,
    private associationService: AdminAssociationService,
    private router: Router,
    private route: ActivatedRoute,
    private snackbar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.associationId = this.route.snapshot.params.id;

    if (this.associationId !== undefined) {
      this.associationService.getAssociation(this.associationId).subscribe(association => {
        this.controlForm.get('name').setValue(association.name);
        this.controlForm.get('description').setValue(association.description);
        this.controlForm.get('founded').setValue(association.founded_on);
        this.controlForm.get('dissolved').setValue(association.dissolved_on);
      });
    }
  }

  onSubmit(): void {
    if (this.controlForm.valid) {
      const nameControl = this.controlForm.get('name');
      const descriptionControl = this.controlForm.get('description');
      const foundedControl = this.controlForm.get('founded');
      const dissolvedControl = this.controlForm.get('dissolved');

      const newAssociation: NewAssociation = {
        name: nameControl.value,
        description: descriptionControl.value || '',
        founded_on: formatDate(foundedControl.value, 'yyyy-MM-dd', 'en-US'),
        dissolved_on:
          dissolvedControl.value !== null
            ? formatDate(dissolvedControl.value, 'yyyy-MM-dd', 'en-US')
            : undefined
      };

      if (this.associationId !== undefined) {
        const association: Association = {
          id: +this.associationId,
          ...newAssociation
        };
        const editAssociation$ = this.associationService.editAssociation(association);

        editAssociation$.subscribe(data => this.onAssociationSaved(data));
      } else {
        const createAssociation$ = this.associationService.createAssociation(newAssociation);

        createAssociation$.subscribe(data => this.onAssociationSaved(data));
      }
    }
  }

  private onAssociationSaved(association: Association): void {
    this.router.navigate(['/ui/admin/associations']);
    this.snackbar.open(`Der Verein '${association.name}' wurde erstellt!`);
  }
}
