import { formatDate } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material';
import { ActivatedRoute, Router } from '@angular/router';
import { NewTeam, Team } from '@frisbee-db-lib/models/team.model';
import { AdminTeamService } from './../../../models/services/admin/team.service.';

@Component({
  selector: 'pm-admin-new-team',
  templateUrl: './admin-new-team.component.html',
  styleUrls: ['./admin-new-team.component.scss'],
  providers: [AdminTeamService]
})
export class AdminNewTeamComponent implements OnInit {
  controlForm = this.fb.group({
    name: [null, Validators.required],
    description: [null],
    founded: [null, Validators.required],
    dissolved: [null]
  });

  teamId: string | undefined;

  constructor(
    private fb: FormBuilder,
    private teamService: AdminTeamService,
    private router: Router,
    private route: ActivatedRoute,
    private snackbar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.teamId = this.route.snapshot.params.id;

    if (this.teamId !== undefined) {
      this.teamService.getTeam(this.teamId).subscribe(team => {
        this.controlForm.get('name').setValue(team.name);
        this.controlForm.get('description').setValue(team.description);
        this.controlForm.get('founded').setValue(team.founded_on);
        this.controlForm.get('dissolved').setValue(team.dissolved_on);
      });
    }
  }

  onSubmit(): void {
    if (this.controlForm.valid) {
      const nameControl = this.controlForm.get('name');
      const descriptionControl = this.controlForm.get('description');
      const foundedControl = this.controlForm.get('founded');
      const dissolvedControl = this.controlForm.get('dissolved');

      const newTeam: NewTeam = {
        name: nameControl.value,
        description: descriptionControl.value || '',
        founded_on: formatDate(foundedControl.value, 'yyyy-MM-dd', 'en-US'),
        dissolved_on:
          dissolvedControl.value !== null
            ? formatDate(dissolvedControl.value, 'yyyy-MM-dd', 'en-US')
            : undefined
      };

      if (this.teamId !== undefined) {
        const team: Team = {
          id: +this.teamId,
          ...newTeam
        };
        const editTeam$ = this.teamService.editTeam(team);

        editTeam$.subscribe(data => this.onTeamSaved(data));
      } else {
        const createTeam$ = this.teamService.createTeam(newTeam);

        createTeam$.subscribe(data => this.onTeamSaved(data));
      }
    }
  }

  private onTeamSaved(team: Team): void {
    this.router.navigate(['/ui/admin/teams']);
    this.snackbar.open(`Das Team '${team.name}' wurde erstellt!`);
  }
}
