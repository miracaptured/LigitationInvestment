import { Injectable } from '@angular/core';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class ApplicationService {

  constructor(
    private _api: ApiService) { }

  getApplications() {
    return this._api.getTypeRequest("applications");
  }
}
