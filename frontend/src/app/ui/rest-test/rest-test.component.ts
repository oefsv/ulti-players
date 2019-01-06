import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';

@Component({
  selector: 'frisbee-rest-test',
  templateUrl: './rest-test.component.html',
  styleUrls: ['./rest-test.component.scss']
})
export class RestTestComponent {
  code = 'Result';
  cookie: string;
  error = false;

  headers: string[];

  @ViewChild('url') url: ElementRef;

  @ViewChild('body') body: ElementRef;

  constructor(private httpClient: HttpClient) {}

  executeGet() {
    var urlElement = this.url.nativeElement as HTMLInputElement;

    this.httpClient
      .request("GET", urlElement.value, {
        //headers: {'Accept': 'application/json'}
        observe: 'response',
        responseType: 'text',
        withCredentials: true,
      })
      .subscribe((data: HttpResponse<string>) => {

         // display its headers
         const keys = data.headers.keys();
         this.headers = keys.map(key =>
           `${key}: ${data.headers.get(key)}`);

        console.log("SUCCESS", data);
        this.code = data.body;
        this.error = false;
        this.checkCookie();
      }, error => {
        this.error = true;
        this.code = JSON.stringify(error);
        console.error("Error", error);
        this.checkCookie();
      });
  }

  checkCookie(): void {
    this.cookie = document.cookie;
  }
}
