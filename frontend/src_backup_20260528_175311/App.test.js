import { render, screen } from '@testing-library/react';
import App from './App.jsx';

test('renders SEN V3 login screen', () => {
  render(<App />);
  expect(screen.getByText(/SEN V3 Engine/i)).toBeInTheDocument();
});
