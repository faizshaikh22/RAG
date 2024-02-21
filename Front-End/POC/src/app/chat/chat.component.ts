import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ChatService } from '../chat.service';
import { trigger, state, style, animate, transition } from '@angular/animations';
import { timeout } from 'rxjs';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css',
  animations: [
    trigger('loadingState', [
      state('in', style({ opacity: 1 })),
      transition(':enter', [
        style({ opacity: 0 }),
        animate(300)
      ]),
      transition(':leave',
        animate(300, style({ opacity: 0 })))
    ])
  ]
})
export class ChatComponent {
  messages: { text: string; sender: string; }[] = [];
  newMessage = '';

  constructor(private chatService: ChatService) { }

  isLoading = false;

  sendMessage() {
    if (!this.isLoading && this.newMessage.trim() !== '') {
      this.isLoading = true;
      this.messages.push({ text: this.newMessage, sender: 'user' });
      this.chatService.sendMessage(this.newMessage)
        .pipe(timeout(25000))
        .subscribe(
          response => {
            this.messages.push({ text: response.output, sender: 'bot' });
            this.isLoading = false;
            this.newMessage = '';
          },
          error => {
            this.messages.push({ text: 'Server not responding. Please try again.', sender: 'bot' });
            this.isLoading = false;
          }
        );
    }
  }
}
