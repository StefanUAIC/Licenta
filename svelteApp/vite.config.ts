import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

const URL = 'http://localhost:5000';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/api': {
				target: `${URL}`,
				changeOrigin: false,
				secure: false
			}
		}
	}
});
