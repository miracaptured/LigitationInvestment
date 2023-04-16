import { Component } from '@angular/core';
import { ApplicationService } from '../services/application.service';
import { UserService } from '../services/user.service';
import { Application } from '../models/application';
import { Router } from '@angular/router';
import { animate, state, style, transition, trigger } from '@angular/animations';

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ])
  ]
})
export class ApplicationsComponent {
  applications: Application[];
  columnsToDisplay: string[] = ['application_id', 'name', 'claim', 'status', 'role'];
  columnsToDisplayWithExpand = [...this.columnsToDisplay, 'expand'];
  expandedElement!: Application | null;

  constructor(private applicationService: ApplicationService, private router: Router) {
    this.applications = [];
  }

  ngOnInit(): void {
    if (!UserService.checkUser()) this.router.navigateByUrl('/');
    
    this.applicationService.getApplications().subscribe((applications: any) => this.applications = applications);
  }
}


