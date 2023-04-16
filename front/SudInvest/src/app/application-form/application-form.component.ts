import { Component, OnInit } from '@angular/core';
import { Application } from '../models/application';
import { MatDialogRef } from '@angular/material/dialog';
import { ApiService } from '../services/api.service';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-application-form',
  templateUrl: './application-form.component.html',
  styleUrls: ['./application-form.component.scss']
})
export class ApplicationFormComponent implements OnInit {

  application!: Application;

  constructor(public dialogRef: MatDialogRef<ApplicationFormComponent>,
              private _api : ApiService) { }

  ngOnInit(): void {
    this.application = new Application(0, UserService.CurrentUser.user_id, "", "на рассмотрении", 0, "истец", "");
  }

  onSubmit(): void {
    try {
      this.addApplication();
      this.dialogRef.close();
    }
    catch {
    }
  }

  addApplication(){ 
    let b = this.application;
    this._api.postTypeRequest('applications', b).subscribe((res: any) => {
          console.log(res);
        }, err => { 
          console.log(err);
        }
    );
  }
}
