<template>
<div>
  <v-data-table
    v-model="selectAll"
    :headers="headers"
    :items="fileInfos"
    item-key="id"
    show-select
    :disable-pagination="true"
    :hide-default-footer="true"
    class="elevation-1"
  >
    <template v-slot:body="props">
      <draggable :list="props.items" tag="tbody">
        <tr
          v-for="(file, index) in props.items"
          v-bind:key="file.id"
          v-bind:title="file.name"
          v-on:remove="file.splice(index, 1)"
        >
          <td>
            <v-checkbox
              id="selectfile"
              :value="file.id"
              v-model="selected"
              hide-details
              class="shrink mr-2 mt-0"
            ></v-checkbox>
          </td>

          <td>{{ index + 1 }}</td>

          <td>
             <!-- <pdf src="/uploads/Dokument_CPR_015f353b6f.pdf"></pdf> -->
            <a :href="file.url">{{ file.file_name }}</a>
          </td>

          <td>
            <v-checkbox
              id="prefixPage"
              :value="file.id"
              v-model="prefixPage"                      
              hide-details
              class="shrink mr-2 mt-0"
              @click="addPrefixPage"
             
            ></v-checkbox>
          </td>

          <td>
            
            <v-icon small @click="deleteDocument(index,file.id)"  >mdi-delete</v-icon>
            <!-- <v-icon small @click="deleteDocument(index,file.id)"  >mdi-delete</v-icon> -->

          </td>
          <td>
            <v-icon small class="page__grab-icon"> mdi-arrow-all </v-icon>
          </td>
        </tr>
      </draggable>
    </template>
  </v-data-table>

  <!-- <div class="text-uppercase text-bold">id selected: {{selected}}</div> -->

    <v-col cols="4" class="pl-2">
      <v-btn color="success" dark small @click="merge"> Merge PDF </v-btn>
    </v-col>

    <v-btn id="downloadmergefile" class="ma-2" outlined v-bind:href="url" download @click="download"> Download PDF </v-btn>


</div>
</template>

<script>
import MergeFileService from "../services/MergeFilesService";
import EditFilesService from "../services/EditFilesService";
import Draggable from "vuedraggable";

export default {
  name: "uploaded-documents-table",

  components: {
    Draggable,
    // pdf
  },
   props:{
      fileInfos: [],
  },
  data() {
    return {
      singleSelect: false,
      selectAll:false,
      prefixPage: [],
      selected: [],
      url: String,

      // fileInfos: [],
      headers: [
        { text: "##", sortable: false },
        {
          text: "Document name",
          align: "start",
          value: "name",
        },
        {text: "Add Prefix Page"},
        { text: "Actions", value: "actions", sortable: false },

        { text: "", sortable: false },
      ],
    };
  },
  methods: {
    select() {
      this.selected = [];
      if (!this.selectAll) {
        for (let i in this.props.items) {
          this.selected.push(this.props.items[i].id);
          console.log(this.selected);
        }
      }
    },

    editDocument(id) {
      this.$router.push({ name: "tutorial-details", params: { id: id } });
    },

    // deleteDocument(id){
    //   console.log(id);
    //   this.fileInfos.splice(id);
    // },

    deleteDocument(index,id) {
      EditFilesService.delete(id)
        .then(() => {
          this.fileInfos.splice(index,1);
          console.log(this.fileInfos);
        })

        .catch((e) => {
          console.log(e);
        });
    },
    
   

    addPrefixPage(){
      EditFilesService.update(this.prefixPage)
    },
    
    merge() {
      if (!this.bundleSize) {
        this.message = "Merge everything into one bundle!";
      }
      console.log(this.selected);

      MergeFileService.merge(this.selected, (response) => {
        console.log(response.data);
        this.url=response.data.url;

        this.bundleSize = "";
      });
    },
    download(){

    }
  }
  // mounted() {
  //   UploadFilesService.getFiles().then((response) => {
  //     this.fileInfos = response.data;
  //     console.log(this.fileInfos);
  //   });
  // },
};
</script>
