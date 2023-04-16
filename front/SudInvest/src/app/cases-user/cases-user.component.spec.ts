import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CasesUserComponent } from './cases-user.component';

describe('CasesUserComponent', () => {
  let component: CasesUserComponent;
  let fixture: ComponentFixture<CasesUserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CasesUserComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CasesUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
