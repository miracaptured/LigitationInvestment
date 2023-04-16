import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

import { User } from '../models/user';
import { UserService } from '../services/user.service';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { AuthService } from '../services/authservice.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  
  user = new User();
  usrpassword!: string;
  constructor(public dialogRef: MatDialogRef<RegisterComponent>,
              private _api : ApiService,
              private router : Router,
              private _auth : AuthService,
              public snackBar: MatSnackBar) { }

  ngOnInit(): void {
  }

  onSubmit(): void {
    try {
      this.register();
    }
    catch {
    }
  }

  register(){ 
    let b = this.user
    console.log(b) 
    this._api.postTypeRequest('register', b).subscribe((res: any) => {
      if (res) {
            this._auth.setDataInLocalStorage('user', res.user);
            this._auth.setDataInLocalStorage('access-token', res.access_token);
            UserService.CurrentUser = res.user;
            this.dialogRef.close();
            this.router.navigate(['/']);
          } 
        }, err => { 
          if (err.status === 401) {
            this.snackBar.open('Ошибка регистрации!', 'Undo', {
              duration: 3000
            });
          } else {
            this.snackBar.open('Ошибка на стороне сервера!'), 'Undo', {
              duration: 3000
            };
          }
        }
    );
  }

}
