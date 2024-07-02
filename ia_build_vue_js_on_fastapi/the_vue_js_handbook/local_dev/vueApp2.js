// vueApp2.js
const { createApp } = Vue
      
createApp({
  data() {
    return { 
        results: {"BTC": {"USD":3759.91,"EUR":3166.21}, "ETH": {"USD":281.7,"EUR":236.25}}
    }
  }
}).mount('#app')