import { Injectable } from '@angular/core';
import { Case } from '../models/case';
import { HttpClient, HttpParams, HttpHeaders, HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map, retry } from 'rxjs/operators';
import { UserService } from './user.service';


const rootUrl : string = 'http://localhost:8000';
const httpObjOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})
export class CaseService {

  constructor(private http: HttpClient) { }

  getCases() : Observable<Case[]> {
    let url = `${rootUrl}/cases/?profile=1&email=${UserService.CurrentUser.email}`;
    let result: Case[] = [];
    return this.http.get<Case[]>(url).pipe(map((data: Case[]) => data));
  }
}
