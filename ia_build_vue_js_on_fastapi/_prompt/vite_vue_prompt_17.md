# vite_vue_prompt_12.md


## prompt

Make the code works when it is loaded in a browser. 

```js
// vueApp5.js
      
const url = "http://127.0.0.1:8000/api/notes/?limit=10&page=1";
const { createApp } = Vue
      
createApp({    
  data() {
    return {
        results:[]
    }
},
    mounted() {
        axios.get(url).then(response => {
            this.results = response.data
        })
  }
}).mount('#app')
```
```txt
Access to XMLHttpRequest at 'http://127.0.0.1:8000/api/notes/?limit=10&page=1' from origin 'null' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Mistral
