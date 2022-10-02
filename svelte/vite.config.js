import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  server: {
		proxy: {
			'/api': 'http://192.168.0.222:8000'
		}
	}
})
