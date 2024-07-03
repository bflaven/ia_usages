/* eslint-disable */
<template>
    <Header />
    <main class="container flex-grow px-4 mx-auto my-12">
        <slot />
    </main>
    <Footer />
</template>

<script>
import Header from "./AppHeader.vue"
import Footer from "./AppFooter.vue"

export default {
    components: {
        Header,
        Footer,
    },
}
</script>