import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private apiUrl = 'http://127.0.0.1:5001/chat';

  constructor(private http: HttpClient) { }

  sendMessage(message: string): Observable<any> {
    const body = { text: message };
    return this.http.post(this.apiUrl, body);
  }
}
