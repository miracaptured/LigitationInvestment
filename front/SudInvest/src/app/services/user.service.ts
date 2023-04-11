import { Injectable } from '@angular/core';
import { User } from '../models/user';
import { HttpClient, HttpParams, HttpHeaders, HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';


const rootUrl : string = 'http://localhost:8000';
const httpObjOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})
export class UserService {

  static CurrentUser : User;

  static checkUser = () => UserService.CurrentUser != null && UserService.CurrentUser != undefined && UserService.CurrentUser.email != "";

  constructor(private http: HttpClient) { }

  private handleError(error: HttpErrorResponse) {
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, body was: `, error.error);
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }

  getUser(email: string) : Observable<User> {
      let url : string = `${rootUrl}/user/?email=${email}`;
      return this.http.get<User>(url).pipe(catchError(this.handleError));
  }

  login(email: string, password: string) {
      let url : string = `${rootUrl}/user/?email=${email}`;
      this.http.get<User>(url).subscribe(data => UserService.CurrentUser = data);
  }

  addUser(user: User) {
    user.profile = user.profile.toLowerCase();
    let url : string = `${rootUrl}/user/`;
    this.http.post<User>(url, user, httpObjOptions).subscribe(data => UserService.CurrentUser = data);
  }
}
