import { formatDate } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material';
import { ActivatedRoute, Router } from '@angular/router';
import { Club, NewClub } from '@frisbee-db-lib/models/club.model';
import { AdminClubService } from '@frisbee-db-lib/services/admin/club.service.';

@Component({
  selector: 'pm-admin-new-club',
  templateUrl: './admin-new-club.component.html',
  styleUrls: ['./admin-new-club.component.scss'],
  providers: [AdminClubService]
})
export class AdminNewClubComponent implements OnInit {
  controlForm = this.fb.group({
    name: [null, Validators.required],
    description: [null],
    founded: [null, Validators.required],
    dissolved: [null]
  });

  clubId: string | undefined;

  constructor(
    private fb: FormBuilder,
    private clubService: AdminClubService,
    private router: Router,
    private route: ActivatedRoute,
    private snackbar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.clubId = this.route.snapshot.params.id;

    if (this.clubId !== undefined) {
      this.clubService.getClub(this.clubId).subscribe(club => {
        this.controlForm.get('name').setValue(club.name);
        this.controlForm.get('description').setValue(club.description);
        this.controlForm.get('founded').setValue(club.founded_on);
        this.controlForm.get('dissolved').setValue(club.dissolved_on);
      });
    }
  }

  onSubmit(): void {
    if (this.controlForm.valid) {
      const nameControl = this.controlForm.get('name');
      const descriptionControl = this.controlForm.get('description');
      const foundedControl = this.controlForm.get('founded');
      const dissolvedControl = this.controlForm.get('dissolved');

      const newClub: NewClub = {
        name: nameControl.value,
        description: descriptionControl.value || '',
        founded_on: formatDate(foundedControl.value, 'yyyy-MM-dd', 'en-US'),
        dissolved_on:
          dissolvedControl.value !== null
            ? formatDate(dissolvedControl.value, 'yyyy-MM-dd', 'en-US')
            : undefined
      };

      if (this.clubId !== undefined) {
        const club: Club = {
          id: +this.clubId,
          ...newClub
        };
        const editClub$ = this.clubService.editClub(club);

        editClub$.subscribe(data => this.onClubSaved(data));
      } else {
        const createClub$ = this.clubService.createClub(newClub);

        createClub$.subscribe(data => this.onClubSaved(data));
      }
    }
  }

  private onClubSaved(club: Club): void {
    this.router.navigate(['/ui/admin/clubs']);
    this.snackbar.open(`Der Verein '${club.name}' wurde erstellt!`);
  }
}
