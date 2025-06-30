import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
  },
  build: {
    rollupOptions: {
      input: {
        main: './index.html',
      },
    },
  },
  // Use test_main.jsx as entry point
  resolve: {
    alias: {
      'src/main.jsx': '/src/test_main.jsx'
    }
  }
});
