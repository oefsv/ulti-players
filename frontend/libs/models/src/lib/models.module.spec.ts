import { async, TestBed } from '@angular/core/testing';
import { ModelsModule } from './models.module';

describe('ModelsModule', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [ModelsModule]
    }).compileComponents();
  }));

  it('should create', () => {
    expect(ModelsModule).toBeDefined();
  });
});
