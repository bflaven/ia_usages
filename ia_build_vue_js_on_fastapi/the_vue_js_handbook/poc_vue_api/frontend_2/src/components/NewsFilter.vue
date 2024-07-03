<template>
    <div class="flex justify-center p-4 rounded">
        <!-- Start of select dropdown -->
        <div class="relative inline-flex">
            <svg class="absolute top-0 right-0 w-2 h-2 m-4 pointer-events-none" xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 412 232">
                <path
                    d="M206 171.144L42.678 7.822c-9.763-9.763-25.592-9.763-35.355 0-9.763 9.764-9.763 25.592 0 35.355l181 181c4.88 4.882 11.279 7.323 17.677 7.323s12.796-2.441 17.678-7.322l181-181c9.763-9.764 9.763-25.592 0-35.355-9.763-9.763-25.592-9.763-35.355 0L206 171.144z"
                    fill="#648299" fill-rule="nonzero" />
            </svg>
            <select
                class="h-10 pl-5 pr-10 text-gray-600 bg-white border border-gray-300 rounded-lg appearance-none hover:border-gray-400 focus:outline-none"
                v-model="section">
                <option v-for="(section, index) in sections" :key="index" :value="section">
                    {{ capitalize(section) }}
                </option>
            </select>
        </div>
        <!-- End of select dropdown -->
        <div class="self-center ml-8">
            <button class="px-6 py-2 text-white bg-green-700 rounded hover:bg-green-900">
                Retrieve
            </button>
        </div>
    </div>
</template>

<script>
import { computed } from "vue"
import sectionsData from "./sections"

export default {
    props: {
        modelValue: String,
    },
    setup(props, { emit }) {
        const section = computed({
            get: () => props.modelValue,
            set: value => emit("update:modelValue", value),
        })

        return {
            section,
        }
    },
    data() {
        return {
            sections: sectionsData,
        }
    },
    methods: {
        capitalize(value) {
            if (!value) return ""
            value = value.toString()
            return value.charAt(0).toUpperCase() + value.slice(1)
        },
    },
}
</script>