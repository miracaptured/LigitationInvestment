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

  user = () => UserService.CurrentUser;

  checkUser = () => UserService.checkUser();

  checkFigurant = () => UserService.checkFigurant();

  casesTitle = () => UserService.checkFigurant() ? 'Мои кейсы' : 'Кейсы';

  constructor(public dialog: MatDialog) {
  }

  ngOnInit(): void {
  }

  openLoginForm() {
    this.dialog.open(LoginComponent, {width: '500px', height: '450px'});
  }
}
