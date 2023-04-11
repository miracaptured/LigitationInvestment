import { Component, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { LoginComponent } from '../login/login.component';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  checkUser = () => UserService.checkUser();

  constructor(public dialog: MatDialog) {
  }

  ngOnInit(): void {
  }

  openLoginForm() {
    this.dialog.open(LoginComponent, {width: '500px', height: '450px'});
  }
}
