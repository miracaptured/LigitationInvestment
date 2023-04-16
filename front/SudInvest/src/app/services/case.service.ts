import { Injectable } from '@angular/core';
import { ApiService } from './api.service';


@Injectable({
  providedIn: 'root'
})
export class CaseService {

  constructor(
    private _api: ApiService
    ) { }

  getCases() {
    return this._api.getTypeRequest("cases");
  }

  getAllCases() {
    return this._api.getTypeRequest("cases/all");
  }
}
