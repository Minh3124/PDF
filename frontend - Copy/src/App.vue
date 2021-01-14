<template>
  <v-app>
  <div class="inline-block tw-space-x-5 ">
  <router-link to="/">Home</router-link>
  <router-link to="/PDF">PDF MERGE</router-link>
  </div>
   <router-view/>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  components: {
  

  },

  data: () => ({
    //
  }),
};

</script>
