import { formatDate } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material';
import { ActivatedRoute, Router } from '@angular/router';
import { NewPerson, Person } from '@frisbee-db-lib/models/person.model';
import { AdminPersonService } from '@frisbee-db-lib/services/admin/person.service';
import { NavigationBarService } from './../../navigation-bar.service';

@Component({
  selector: 'pm-admin-new-person',
  templateUrl: './admin-new-person.component.html',
  styleUrls: ['./admin-new-person.component.scss'],
  providers: [AdminPersonService]
})
export class AdminNewPersonComponent implements OnInit {
  controlForm = this.fb.group({
    firstname: [undefined, Validators.required],
    lastname: [undefined, Validators.required],
    sex: [undefined],
    birthdate: [undefined, Validators.required]
  });

  personId: string | undefined;

  constructor(
    private readonly fb: FormBuilder,
    private readonly personService: AdminPersonService,
    private readonly router: Router,
    private readonly route: ActivatedRoute,
    private readonly snackbar: MatSnackBar,
    private readonly navigationBarService: NavigationBarService
  ) {}

  ngOnInit(): void {
    this.navigationBarService.setTitle('Neue Person');
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
      const sexControl = this.controlForm.get('sex');

      const newPerson: NewPerson = {
        firstname: firstNameControl.value,
        lastname: lastNameControl.value,
        sex: sexControl.value,
        birthdate: formatDate(birthdateControl.value, 'yyyy-MM-dd', 'en-US')
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
