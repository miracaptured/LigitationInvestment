import { Component, OnInit } from '@angular/core'; 
import { AuthService } from '../services/authservice.service';
import { ApiService } from '../services/api.service';
import { User } from '../models/user';
import { Case } from '../models/case';
import { ApplicationFormComponent } from '../application-form/application-form.component';
import { MatDialog } from '@angular/material/dialog';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';
 
@Component({ 
  selector: 'app-profile', 
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'] 
}) 
export class ProfileComponent implements OnInit {

  user!: User;
  cases: Case[] = [];
  errorMsg!: string;

  constructor( 
    private _api : ApiService, 
    private _auth: AuthService,
    private router: Router,
    public dialog: MatDialog
  ) { } 
 
  ngOnInit(): void {
    if (!UserService.checkUser()) this.router.navigateByUrl('/');
    
    this.loadInfo();
  }
 
  loadInfo() {
    this.user = UserService.CurrentUser;
  }

  logout() {
    this._auth.clearStorage();
    this.router.navigateByUrl('/home');
  }

  openAppForm() {
    this.dialog.open(ApplicationFormComponent, {width: '500px', height: '450px'});
  }
}