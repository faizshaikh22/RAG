import { Component, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-files',
  templateUrl: './files.component.html',
  styleUrls: ['./files.component.css']
})
export class FilesComponent {

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
  }

  onChangeFile(event: any) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.uploadFile(file);
    }
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    const file = event.dataTransfer?.files[0];
    if (file) {
      this.uploadFile(file);
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
  }

  private uploadFile(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    this.http.post('http://127.0.0.1:5000/upload', formData).subscribe({
      next: (response) => {
        console.log(response);
        alert('File uploaded successfully!');
      },
      error: (error) => {
        console.error(error);
        if (error.error && error.error.error) {
          alert(error.error.error);
        } else {
          alert('An error occurred while uploading the file.');
        }
      }
    });
  }
}
