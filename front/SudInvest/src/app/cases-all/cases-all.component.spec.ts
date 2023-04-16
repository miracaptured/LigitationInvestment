import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CasesAllComponent } from './cases-all.component';

describe('CasesAllComponent', () => {
  let component: CasesAllComponent;
  let fixture: ComponentFixture<CasesAllComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CasesAllComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CasesAllComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
