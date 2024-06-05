import preprocess from 'svelte-preprocess';
import adapter from '@sveltejs/adapter-auto';
import path from 'path';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: preprocess({
    postcss: true,
    typescript: true,
  }),

  kit: {
    adapter: adapter(),
    alias: {
      $lib: path.resolve('./src/lib')
    }
  }
};

export default config;
