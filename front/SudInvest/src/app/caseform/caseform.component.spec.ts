import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CaseformComponent } from './caseform.component';

describe('CaseformComponent', () => {
  let component: CaseformComponent;
  let fixture: ComponentFixture<CaseformComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CaseformComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CaseformComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
