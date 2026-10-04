import react from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react({ jsxRuntime: 'automatic' })],
  ...(mode === 'test' ? { esbuild: { jsx: 'automatic' } } : {}),
  test: {
    environment: 'jsdom',
    setupFiles: './src/testSetup.js',
    base: '/devops_cicd_courses/',   // le nom du dépôt, avec les deux slashs
  },
}))
