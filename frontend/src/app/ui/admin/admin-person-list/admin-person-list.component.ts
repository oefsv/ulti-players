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
import { Person } from '@frisbee-db-lib/models/person.model';
import { AdminPersonService } from '@frisbee-db-lib/services/admin/person.service.';
import { of } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';

@Component({
  selector: 'pm-admin-person-list',
  templateUrl: './admin-person-list.component.html',
  styleUrls: ['./admin-person-list.component.scss'],
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
  providers: [AdminPersonService]
})
export class AdminPersonListComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  dataSource: MatTableDataSource<Person>;

  isLoadingResults = true;

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['lastname', 'firstname'];
  expandedElement: Person | null;

  _personService: AdminPersonService;

  constructor(
    private personService: AdminPersonService,
    private snackbar: MatSnackBar
  ) {
    this._personService = personService;
  }

  ngOnInit(): void {
    this.dataSource = new MatTableDataSource();
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;

    of({})
      .pipe(
        switchMap(() => {
          this.isLoadingResults = true;

          return this._personService.getPersons();
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

  onDelete(person: Person): void {
    this.personService.deletePerson(person).subscribe(result => {
      this.snackbar.open(
        `Die Person '${person.lastname} ${person.firstname}' wurde gelöscht!`
      );
      this.dataSource.data = this.dataSource.data.filter(
        obj => obj.id !== person.id
      );
    });
  }
}
