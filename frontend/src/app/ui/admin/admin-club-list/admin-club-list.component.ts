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
import { Club } from '@frisbee-db-lib/models/club.model';
import { AdminClubService } from '@frisbee-db-lib/services/admin/club.service.';
import { of } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';
import { NavigationBarService } from './../../navigation-bar.service';

@Component({
  selector: 'pm-admin-club-list',
  templateUrl: './admin-club-list.component.html',
  styleUrls: ['./admin-club-list.component.scss'],
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
  providers: [AdminClubService]
})
export class AdminClubListComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  dataSource: MatTableDataSource<Club>;

  isLoadingResults = true;

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['id', 'name'];
  expandedElement: Club | null;

  constructor(
    private readonly clubService: AdminClubService,
    private readonly snackbar: MatSnackBar,
    private readonly navigationBarService: NavigationBarService
  ) {}

  ngOnInit(): void {
    this.navigationBarService.setTitle('Vereine (Admin)');
    this.dataSource = new MatTableDataSource();
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;

    of({})
      .pipe(
        switchMap(() => {
          this.isLoadingResults = true;

          return this.clubService.getClubs();
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

  onDelete(club: Club): void {
    this.clubService.deleteClub(club).subscribe(result => {
      this.snackbar.open(`Der Verein '${club.name}' wurde gelöscht!`);
      this.dataSource.data = this.dataSource.data.filter(
        obj => obj.id !== club.id
      );
    });
  }
}
