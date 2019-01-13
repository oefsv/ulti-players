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
import { Association } from '@frisbee-db-lib/models/association.model';
import { AdminAssociationService } from '@frisbee-db-lib/services/admin/association.service.';
import { of } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';

@Component({
  selector: 'pm-admin-association-list',
  templateUrl: './admin-association-list.component.html',
  styleUrls: ['./admin-association-list.component.scss'],
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
  providers: [AdminAssociationService]
})
export class AdminAssociationListComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  dataSource: MatTableDataSource<Association>;

  isLoadingResults = true;

  displayedColumns = ['id', 'name'];
  expandedElement: Association | null;

  _associationService: AdminAssociationService;

  constructor(
    private associationService: AdminAssociationService,
    private snackbar: MatSnackBar
  ) {
    this._associationService = associationService;
  }

  ngOnInit(): void {
    this.dataSource = new MatTableDataSource();
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;

    of({})
      .pipe(
        switchMap(() => {
          this.isLoadingResults = true;

          return this._associationService.getAssociations();
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

  onDelete(association: Association): void {
    this.associationService.deleteAssociation(association).subscribe(result => {
      this.snackbar.open(`Der Verband '${association.name}' wurde gelöscht!`);
      this.dataSource.data = this.dataSource.data.filter(
        obj => obj.id !== association.id
      );
    });
  }
}
