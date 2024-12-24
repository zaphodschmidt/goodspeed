import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import dotenv from 'dotenv';

dotenv.config(); // Load environment variables from .env file

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
  define: {
    'process.env': process.env, // Pass all environment variables to the frontend
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
})
