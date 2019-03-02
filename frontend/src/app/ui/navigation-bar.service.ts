import { Inject, Injectable } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NavigationBarService {
  readonly currentTitle$ = new BehaviorSubject('');

  constructor(private readonly titleService: Title) {
    this.titleService.setTitle('ulti-players');
  }

  setTitle(title: string): void {
    this.currentTitle$.next(title);
    this.titleService.setTitle(`ulti-players - ${title}`);
  }
}
