import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing/app-routing.module';
import { AppComponent } from './app.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar'; 
import { MatListModule } from '@angular/material/list';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { MAT_DIALOG_DEFAULT_OPTIONS, MatDialogModule } from '@angular/material/dialog'; 
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox'
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatNativeDateModule} from '@angular/material/core';
import { MatRadioModule } from '@angular/material/radio';
import { MatGridListModule } from '@angular/material/grid-list';
import {MatTableModule} from '@angular/material/table';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIconModule} from '@angular/material/icon';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatSnackBarModule} from '@angular/material/snack-bar';


import { FlexLayoutModule } from '@angular/flex-layout';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';


import 'hammerjs';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ProfileComponent } from './profile/profile.component';
import { CasesComponent } from './cases/cases.component';
import { CaseformComponent } from './caseform/caseform.component';
import { RegisterComponent } from './register/register.component';
import { CaseinfoComponent } from './caseinfo/caseinfo.component';
import { ApplicationsComponent } from './applications/applications.component';
import { InterceptorService } from './services/interceptor-service.service';
import { ApplicationFormComponent } from './application-form/application-form.component';
import { FaqComponent } from './faq/faq.component';
import { CasesAllComponent } from './cases-all/cases-all.component';
import { CasesUserComponent } from './cases-user/cases-user.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    LoginComponent,
    HomeComponent,
    ProfileComponent,
    CasesComponent,
    CaseformComponent,
    RegisterComponent,
    CaseinfoComponent,
    ApplicationsComponent,
    ApplicationFormComponent,
    FaqComponent,
    CasesAllComponent,
    CasesUserComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    FlexLayoutModule,
    MatListModule,
    MatFormFieldModule,
    MatDialogModule,
    FormsModule,
    FontAwesomeModule,
    MatButtonModule,
    MatCardModule,
    MatInputModule,
    MatCheckboxModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatRadioModule,
    MatGridListModule,
    MatTableModule,
    MatExpansionModule,
    MatIconModule,
    MatSlideToggleModule,
    MatSnackBarModule
  ],
  providers: [ //UserService, CaseService,
  { provide: HTTP_INTERCEPTORS, useClass: InterceptorService, multi: true },
  { provide: MAT_DIALOG_DEFAULT_OPTIONS, useValue: {hasBackdrop: false} }
  ],
  entryComponents: [
    LoginComponent,
    RegisterComponent,
    ApplicationFormComponent
  ],
  bootstrap: [AppComponent],
  exports: [AppRoutingModule]
})
export class AppModule {}
