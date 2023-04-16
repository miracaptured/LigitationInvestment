import { Component, Inject, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-caseform',
  templateUrl: './caseform.component.html',
  styleUrls: ['./caseform.component.scss']
})
export class CaseformComponent implements OnInit {
  investment!: Investment;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: {case_id: number},
    public dialogRef: MatDialogRef<CaseformComponent>,
    private _api : ApiService,
    private router : Router,
    public snackBar: MatSnackBar) {
      this.investment = new Investment();
      this.investment.case_id = data.case_id;
    }

  ngOnInit(): void {
  }

    onSubmit(): void {
      try {
        this.invest();
        this.dialogRef.close();
        this.router.navigateByUrl('/cases');
      } catch {
      }
    }

    invest() {
      this._api.postTypeRequest('invest', this.investment).subscribe((res: any) => {
        this.snackBar.open('Заявка оформлена!', 'Скрыть', {
          duration: 3000
        });
      });
      
    }
}

class Investment {
  money!: number;
  case_id: number = 0;
}