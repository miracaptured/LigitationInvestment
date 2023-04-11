import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

import { User } from '../models/user';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  
  user = new User();
  constructor(public dialogRef: MatDialogRef<RegisterComponent>,
              private userService: UserService) { }

  ngOnInit(): void {
  }

  onSubmit(): void {
    try {
      this.userService.addUser(this.user);
      this.dialogRef.close();
    }
    catch {
      
    }
  }

}
