import { Component, OnInit, Inject } from '@angular/core';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';
import {animate, state, style, transition, trigger} from '@angular/animations';

@Component({
  selector: 'app-cases',
  templateUrl: './cases.component.html',
  styleUrls: ['./cases.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ])
  ]
})
export class CasesComponent implements OnInit {

  showAll: boolean = false;
  checkFigurant = () => UserService.checkFigurant();
  checkboxTitle = "мои дела";

  constructor(private router: Router) { }

  ngOnInit(): void {
    if (!UserService.checkUser()) this.router.navigateByUrl('/');
  }

  onShowModeChanged() {
    if (this.showAll) this.checkboxTitle = "все дела";
    else this.checkboxTitle = "мои дела";
  }

  

}
