import { Component, OnInit, ViewChild, Inject} from '@angular/core';
import { Params, ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { CaseService } from '../services/case.service';
import { switchMap } from 'rxjs/operators';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Case } from '../models/case';

@Component({
  selector: 'app-caseinfo',
  templateUrl: './caseinfo.component.html',
  styleUrls: ['./caseinfo.component.scss']
})
export class CaseinfoComponent {
  case!: Case;
  @ViewChild('fform') commentFormDirective: any;

  constructor (private caseService: CaseService,
    @Inject('baseURL') private baseURL : any) {}

    ngOnInit() {
    }
}
