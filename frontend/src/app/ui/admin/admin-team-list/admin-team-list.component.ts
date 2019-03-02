import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';
import { Component, OnInit, ViewChild } from '@angular/core';
import {
  MatPaginator,
  MatSnackBar,
  MatSort,
  MatTableDataSource
} from '@angular/material';
import { Team } from '@frisbee-db-lib/models/team.model';
import { AdminTeamService } from '@frisbee-db-lib/services/admin/team.service.';
import { of } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';
import { NavigationBarService } from './../../navigation-bar.service';

@Component({
  selector: 'pm-admin-team-list',
  templateUrl: './admin-team-list.component.html',
  styleUrls: ['./admin-team-list.component.scss'],
  animations: [
    trigger('detailExpand', [
      state(
        'collapsed',
        style({ height: '0px', minHeight: '0', display: 'none' })
      ),
      state('expanded', style({ height: '*' })),
      transition(
        'expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
      )
    ])
  ],
  providers: [AdminTeamService]
})
export class AdminTeamListComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  dataSource: MatTableDataSource<Team>;

  isLoadingResults = true;

  displayedColumns = ['id', 'name'];
  expandedElement: Team | null;

  constructor(
    private readonly teamService: AdminTeamService,
    private readonly snackbar: MatSnackBar,
    private readonly navigationBarService: NavigationBarService
  ) {}

  ngOnInit(): void {
    this.navigationBarService.setTitle('Teams (Admin)');
    this.dataSource = new MatTableDataSource();
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;

    of({})
      .pipe(
        switchMap(() => {
          this.isLoadingResults = true;

          return this.teamService.getTeams();
        }),
        map(data => {
          this.isLoadingResults = false;

          return data;
        })
      )
      .subscribe(data => {
        this.dataSource.data = data;
      });
  }

  applyFilter(filterValue: string): void {
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  onDelete(team: Team): void {
    this.teamService.deleteTeam(team).subscribe(result => {
      this.snackbar.open(`Der Verband '${team.name}' wurde gelöscht!`);
      this.dataSource.data = this.dataSource.data.filter(
        obj => obj.id !== team.id
      );
    });
  }
}
