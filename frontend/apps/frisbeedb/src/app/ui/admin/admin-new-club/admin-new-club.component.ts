import { formatDate } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { AdminClubService } from '@frisbee-db-lib/services/admin/club.service.';
import { NewClub } from './../../../../../../../libs/models/src/lib/models/club.model';

@Component({
  selector: 'frisbee-admin-new-club',
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
    private route: ActivatedRoute
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
        dissolved_on: formatDate(dissolvedControl.value, 'yyyy-MM-dd', 'en-US')
      };

      const createClub$ = this.clubService.createClub(newClub);

      createClub$.subscribe(data => {
        alert('created');
        console.log(data);
      });
    }
  }
}
