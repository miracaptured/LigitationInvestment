import { Component, OnInit, Inject } from '@angular/core';
import { Case } from '../models/case';
import { CaseService } from '../services/case.service';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-cases',
  templateUrl: './cases.component.html',
  styleUrls: ['./cases.component.scss']
})
export class CasesComponent implements OnInit {
  cases: Case[];

  constructor(private caseService: CaseService) {
    this.cases = [];
  }

  ngOnInit(): void {
    if (UserService.checkUser())
      this.caseService.getCases().subscribe((cases: Case[]) => this.cases = cases);
  }

}
