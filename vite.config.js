import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [],
  server: {
    proxy: {
      // Proxy all /api/chem requests to the chemistry API server
      '/api/chem': {
        target: 'http://10.0.0.149:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/chem/, ''),
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id) return;

          if (id.includes('/js/data/locales/ui/')) return 'ui-locales';
          if (id.includes('/js/data/locales/ions/')) return 'ion-locales';
          if (id.includes('/js/data/locales/')) return 'element-locales';
        },
      },
    },
  },
});
