import { Component, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';

import { User } from '../models/user';
import { RegisterComponent } from '../register/register.component';
import { UserService } from '../services/user.service';
import { ApiService } from '../services/api.service';
import { AuthService } from '../services/authservice.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  constructor(public dialogRef: MatDialogRef<LoginComponent>,
              public dialog: MatDialog,
              private _api : ApiService, 
              private _auth: AuthService,
              private router: Router,
              public snackBar: MatSnackBar) { }

  user = new User();

  ngOnInit(): void {
  }

  onSubmit(): void {
    try {
      this.login();
    } catch {
    }
  }

  openRegForm() {
    this.dialog.open(RegisterComponent, {width: '600px', height: '600px'});
    this.dialogRef.close();
  }

  login(){ 
    let b = this.user
    console.log(b) 
    this._api.postTypeRequest('login', {"email": b.email, "password": b.password}).subscribe((res: any) => { 
      console.log(res) 
      if(res.access_token){ 
        this._auth.setDataInLocalStorage('access-token', res.access_token);
        this._auth.setDataInLocalStorage('user', res.user);
        UserService.CurrentUser = res.user;
        this.dialogRef.close();
        this.router.navigate(['/']);
      } 
    }, err => { 
      if (err.status === 401) {
        this.snackBar.open('Ошибка авторизации!', 'Скрыть', {
          duration: 3000
        });
      } else {
        this.snackBar.open('Ошибка на стороне сервера!', 'Скрыть', {
          duration: 3000
        });
      }
    });
  } 

}
