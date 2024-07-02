// vueApp6.js
      
const url = "http://localhost:5555/posts";
            const { createApp } = Vue;

            createApp({
                data() {
                    return {
                        results: []
                    };
                },
                mounted() {
                    axios.get(url, { mode: 'cors' }).then(response => {
                        this.results = response.data;
                        console.log("GOT DATA");
                    }).catch(error => {
                        console.error("There was an error!", error);
                    });
                }
            }).mount('#app');