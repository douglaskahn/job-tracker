import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Get the port from environment variable or default to 4000
const port = parseInt(process.env.VITE_PORT || '4000');

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: port,
    strictPort: true,
    host: 'localhost'
  }
});
