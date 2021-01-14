<template>
  <div id="app">
    <upload-files></upload-files>
  </div>
</template>

<script>
// import Button from '../components/Button'
import UploadFiles from "../components/UploadDocumentInput";
import "tailwindcss/tailwind.css";
// import Input from "../components/inputFileSize.vue";

import axios from "axios";
import Vue from "vue";

Vue.prototype.$http = axios;

export default {
  name: "App",
  components: {
    UploadFiles,
  },

  methods: {
    openExplorer() {},

    uploadPDF() {},

    mergePDF() {},

    generateFrontPage() {},

    generateTOC() {},

    splitPDF() {},
  },
};
</script>
