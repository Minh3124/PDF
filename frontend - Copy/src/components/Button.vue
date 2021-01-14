<template>
<div class="ml-3 inline-flex rounded-md shadow">
    <button class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50">{{label}}</button>
</div>
</template>


<script>

export default {
  name: 'Button',
  props: {
    label: String
  }
}
</script>
