import { Component, OnInit } from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';
import { Case } from '../models/case';
import { CaseService } from '../services/case.service';
import { MatDialog } from '@angular/material/dialog';
import { CaseformComponent } from '../caseform/caseform.component';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-cases-all',
  templateUrl: './cases-all.component.html',
  styleUrls: ['./cases-all.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ])
  ]
})
export class CasesAllComponent implements OnInit {
  cases: Case[];
  columnsToDisplay: string[] = ['case_id', 'name', 'status', 'claim', 'investment'];
  columnsToDisplayWithExpand = [...this.columnsToDisplay, 'expand'];
  expandedElement!: Case | null;

  checkInvestor = () => !UserService.checkFigurant();

  constructor(private caseService: CaseService, private dialog: MatDialog) {
    this.cases = [];
  }
  ngOnInit(): void {
    this.getCases();
  }

  private getCases() {
    this.caseService.getAllCases().subscribe((res: any) => this.cases = res as Case[]);
  }

  invest(case_id: number) {
    let dialogRef = this.dialog.open(CaseformComponent, {width: '600px', height: '600px', data: { case_id: case_id }});
    dialogRef.afterClosed().subscribe(() => this.getCases());
  }

}
