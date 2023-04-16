import { Routes } from '@angular/router';

import { HomeComponent } from '../home/home.component';
import { CasesComponent } from '../cases/cases.component';
import { ProfileComponent } from '../profile/profile.component';
import { CaseinfoComponent } from '../caseinfo/caseinfo.component';
import { ApplicationsComponent } from '../applications/applications.component';
import { FaqComponent } from '../faq/faq.component';

export const routes: Routes = [
    {path: 'home', component: HomeComponent},
    {path: 'user', component: ProfileComponent},
    {path: 'cases', component: CasesComponent},
    {path: 'applications', component: ApplicationsComponent},
    {path: 'faq', component: FaqComponent},
    //{path: 'cases/:id', component: CaseinfoComponent}
    {path: '', redirectTo: '/home', pathMatch: 'full'}
];