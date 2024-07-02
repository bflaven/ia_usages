// vueApp4.js
      
const url = "https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD,EUR";
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