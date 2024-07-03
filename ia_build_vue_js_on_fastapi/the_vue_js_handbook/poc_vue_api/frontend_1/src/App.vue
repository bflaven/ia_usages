<template>
    <Layout>

        <h2 class="mb-8 text-4xl font-bold text-center capitalize">
            POC_1 News Section : <span class="text-green-700">{{ section }}</span>
        </h2>
        <NewsFilter v-model="section" />
        <NewsList :posts="posts" />
    </Layout>
</template>

<script>
import Layout from "./components/AppLayout.vue"
import NewsFilter from "./components/NewsFilter.vue"
import NewsList from "./components/NewsList.vue"

import data from "./posts.json"

export default {
    components: {
        Layout,
        NewsFilter,
        NewsList,
    },
    data() {
        return {
            section: "home",
            posts: data.posts,
        }
    },
}
</script>