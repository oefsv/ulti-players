import { formatDate } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material';
import { ActivatedRoute, Router } from '@angular/router';
import { NewPerson, Person } from '@frisbee-db-lib/models/person.model';
import { AdminPersonService } from '@frisbee-db-lib/services/admin/person.service.';

@Component({
  selector: 'pm-admin-new-person',
  templateUrl: './admin-new-person.component.html',
  styleUrls: ['./admin-new-person.component.scss'],
  providers: [AdminPersonService]
})
export class AdminNewPersonComponent implements OnInit {
  controlForm = this.fb.group({
    firstname: [null, Validators.required],
    lastname: [null, Validators.required],
    sex: [null],
    birthdate: [null, Validators.required]
  });

  personId: string | undefined;

  constructor(
    private fb: FormBuilder,
    private personService: AdminPersonService,
    private router: Router,
    private route: ActivatedRoute,
    private snackbar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.personId = this.route.snapshot.params.id;

    if (this.personId !== undefined) {
      this.personService.getPerson(this.personId).subscribe(person => {
        this.controlForm.get('firstname').setValue(person.firstname);
        this.controlForm.get('lastname').setValue(person.lastname);
        this.controlForm.get('birthdate').setValue(person.birthdate);
        this.controlForm.get('sex').setValue(person.sex);
      });
    }
  }

  onSubmit(): void {
    if (this.controlForm.valid) {
      const firstNameControl = this.controlForm.get('firstname');
      const lastNameControl = this.controlForm.get('lastname');
      const birthdateControl = this.controlForm.get('birthdate');
      // const dissolvedControl = this.controlForm.get('dissolved');

      const newPerson: NewPerson = {
        firstname: firstNameControl.value,
        lastname: lastNameControl.value,
        sex: 'm',
        birthdate: formatDate(birthdateControl.value, 'yyyy-MM-dd', 'en-US')
        // description: descriptionControl.value || '',
        // dissolved_on:
        //   dissolvedControl.value !== null
        //     ? formatDate(dissolvedControl.value, 'yyyy-MM-dd', 'en-US')
        //     : undefined
      };

      if (this.personId !== undefined) {
        const person: Person = {
          id: +this.personId,
          ...newPerson
        };
        const editPerson$ = this.personService.editPerson(person);

        editPerson$.subscribe(data => this.onPersonSaved(data));
      } else {
        const createPerson$ = this.personService.createPerson(newPerson);

        createPerson$.subscribe(data => this.onPersonSaved(data));
      }
    }
  }

  private onPersonSaved(person: Person): void {
    this.router.navigate(['/ui/admin/persons']);
    this.snackbar.open(
      `Die Person '${person.lastname} ${person.firstname}' wurde erstellt!`
    );
  }
}
