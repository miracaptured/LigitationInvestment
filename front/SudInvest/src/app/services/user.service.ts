import { Injectable } from '@angular/core';
import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  static CurrentUser : User;

  static checkUser = () => localStorage.getItem("user") != null && UserService.CurrentUser != undefined;

  static checkFigurant = () => localStorage.getItem("user") != null && UserService.CurrentUser != undefined && UserService.CurrentUser.profile != "инвестор"; 
}
