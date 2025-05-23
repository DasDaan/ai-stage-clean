import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Voor template-driven forms
import { HttpClientModule } from '@angular/common/http'; // Voor API-verzoeken
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule], // Voeg benodigde modules toe
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.scss'] // Let op: gebruik 'styleUrls' (meervoud)
})
export class ContactComponent {
  formData = {
    first_name: '',
    last_name: '',
    email: '',
    message: ''
  };

  isLoading = false;
  successMessage = '';
  errorMessage = '';

  constructor(private http: HttpClient) {}

  onSubmit() {
    this.isLoading = true;
    this.http.post('http://localhost:3000/api/contact', this.formData).subscribe(
      (response) => {
        this.isLoading = false;
        this.successMessage = 'Your message has been sent!';
        this.errorMessage = ''; // Zorg ervoor dat de foutmelding wordt gereset
        this.formData = { first_name: '', last_name: '', email: '', message: '' }; // Reset het formulier

        // Verwijder de succesmelding na 4 seconden
        setTimeout(() => {
          this.successMessage = '';
        }, 4000);
      },
      (error) => {
        this.isLoading = false;
        this.errorMessage = 'There was an error sending your message. Please try again.';
        this.successMessage = ''; // Zorg ervoor dat de succesmelding wordt gereset

        // Verwijder de foutmelding na 4 seconden
        setTimeout(() => {
          this.errorMessage = '';
        }, 4000);
      }
    );
  }
}
