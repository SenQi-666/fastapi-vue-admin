import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path';

console.log(resolve)
// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd());
  return {
    plugins: [vue()],
    server:{
      host: '0.0.0.0',
      port: 5180,
      proxy: {
        [env.VITE_APP_BASE_API]: {
          target: env.VITE_API_BASE_URL,
          changeOrigin: true
        }
      }
    },
    resolve: {
      alias: {
        '@': resolve(__dirname, './src')
      }
    }
  }
})
