<template>
    <div>
        <h1>API V2</h1>
        <h2 v-for="e in examples" :key="e.id">
            {{ e.id }} - {{ e.example }}
        </h2>
    </div>
</template>

<script>
import { ref } from 'vue'

export default {
    setup() {
        const examples = ref([])

        const load = async () => {
            try {
                const response = await fetch("http://127.0.0.1:8000/things", {
                    method: "GET",
                    // Change to 'cors' to allow cross-origin requests
                    mode: 'cors' 
                })


                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                examples.value = await response.json()
                
            } catch (error) {
                console.error('There was a problem with your fetch operation:', error);
            }
        }

        load()

        return { examples }
    }
}
</script>
