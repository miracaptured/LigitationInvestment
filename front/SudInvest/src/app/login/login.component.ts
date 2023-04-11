import { Component, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';

import { User } from '../models/user';
import { RegisterComponent } from '../register/register.component';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  constructor(public dialogRef: MatDialogRef<LoginComponent>,
              public dialog: MatDialog,
              private userService: UserService) { }

  user = new User();

  ngOnInit(): void {
  }

  onSubmit(): void {
    try {
      this.userService.login(this.user.email, this.user.password);
      this.dialogRef.close();
    } catch {
    }
  }

  openRegForm() {
    this.dialog.open(RegisterComponent, {width: '600px', height: '600px'});
    this.dialogRef.close();
  }

}
