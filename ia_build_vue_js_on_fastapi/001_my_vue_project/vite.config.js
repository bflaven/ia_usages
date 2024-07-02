/*

- go to path
cd /Users/brunoflaven/Documents/01_work/blog_articles/build_vue_js_on_fastapi/001_my_vue_project


- launch the dev
npm run dev
Check http://localhost:5173/

- launch the build
npm run build
npm run preview
Check http://localhost:4173/

- CAUTION: if you want to use the commnds vite 
npm install -g vite

- For dev
vite

- For build
vite build

- For preview or serve
vite preview
 */


import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import axios from 'axios'


// https://vitejs.dev/config/
/*
export default defineConfig({
  plugins: [vue()],
  devServer: {
    proxy: {
      '^/things': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true
      },
    }
  },
})
*/

export default defineConfig({
  plugins: [vue()],
})