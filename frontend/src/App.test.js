import { render, screen } from '@testing-library/react';
import App from './App';

test('renders TalkGuest header', () => {
  render(<App />);
  const headerElement = screen.getByText(/TalkGuest Analytics/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders Upload tab by default', () => {
  render(<App />);
  const uploadTab = screen.getByText(/Upload & Process/i);
  expect(uploadTab).toBeInTheDocument();
});

test('renders file upload section', () => {
  render(<App />);
  const uploadSection = screen.getByText(/Upload Data Files/i);
  expect(uploadSection).toBeInTheDocument();
});

test('shows guests list dropzone', () => {
  render(<App />);
  const guestsLabel = screen.getByText(/Guests List/i);
  expect(guestsLabel).toBeInTheDocument();
});

test('shows reservations dropzone', () => {
  render(<App />);
  const reservationsLabel = screen.getByText(/Reservations/i);
  expect(reservationsLabel).toBeInTheDocument();
});

test('shows invoices dropzone', () => {
  render(<App />);
  const invoicesLabel = screen.getByText(/Invoices/i);
  expect(invoicesLabel).toBeInTheDocument();
});
