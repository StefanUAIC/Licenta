import { join } from 'path';
import type { Config } from 'tailwindcss';

import { skeleton } from '@skeletonlabs/tw-plugin';


const config = {
	darkMode: 'class',
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		join(require.resolve(
				'@skeletonlabs/skeleton'),
			'../**/*.{html,js,svelte,ts}'
		)
	],
	theme: {
		extend: {
			colors: {
				indigo: {
					600: '#4f46e5',
					700: '#344ba0'
				},
				teal: {
					500: '#46d6e5',
					600: '#3196a0'
				}
			}
		}

	},

	plugins: [
		skeleton({
			themes: { preset: ['skeleton'] }
		})
	]


} satisfies Config;

export default config;
						