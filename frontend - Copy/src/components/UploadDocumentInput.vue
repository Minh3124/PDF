<template v-slot:top>
  <div>
    <div v-if="currentFile">
      <div>
        <v-progress-linear
          v-model="progress"
          color="light-blue"
          height="25"
          reactive
        >
          <strong>{{ progress }} %</strong>
        </v-progress-linear>
      </div>
    </div>

    <v-alert v-if="message" border="right" color="blue-grey" dark>
      {{ message }}
    </v-alert>

    <v-row no-gutters justify="center" a lign="center">
      <v-col cols="8">
        <v-file-input
          multiple
          show-size
          label="File input"
          @change="selectFile"
          enctype="multipart/form-data"
        ></v-file-input>
      </v-col>

      <v-col cols="4" class="pl-2">
        <v-btn color="success" dark small @click="upload">
          Upload
          <v-icon right dark>mdi-cloud-upload</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="1" class="pl-3">
        <v-subheader>Max size for bundle:</v-subheader>
      </v-col>
      <v-col cols="2">
        <v-text-field label="bundleSize" value="" suffix="MB"></v-text-field>
      </v-col>
    </v-row>

    <uploaded-documents-table :fileInfos="fileInfos"></uploaded-documents-table>

  </div>
</template>

<script>
import UploadFilesService from "../services/UploadFilesService";
import UploadedDocumentsTable from "../components/UploadedDocumentsTable.vue";

export default {
  name: "upload-files",

  components: {
    UploadedDocumentsTable,
  },
  data() {
    return {
      bundleSize: undefined,
      currentFile: undefined,
      progress: 0,
      message: "",
      fileInfos: [],
      downloadfile:[],
    };
  },
  methods: {
    selectFile(file) {
      this.progress = 0;
      this.currentFile = file;
      console.log(this.currentFile);
    },

    upload() {
      if (!this.currentFile) {
        this.message = "Please select a file!";
        return;
      }

      this.message = "";

      UploadFilesService.upload(this.currentFile, (event) => {
        this.progress = Math.round((100 * event.loaded) / event.total);
        console.log(this.progress + this.currentFile);
      })

        .then((response) => {
          this.fileInfos = response.data
          UploadFilesService.getFiles().then((response) => {
            this.fileInfos = response.data;
            console.log(this.fileInfos);
          });
          this.message = "Uploaded";
        
        })

        .catch(() => {
          this.progress = 0;
          this.message = "Could not upload the file!";
          this.currentFile = undefined;
        });
    }

  },
  mounted() {
    UploadFilesService.getFiles().then((response) => {
      this.fileInfos = response.data;
      console.log(this.fileInfos);
    });
  },
};

// export default {
//   name: "Document",
//   data() {
//     // return {
//     //   documents: [],
//     // };
//     return {
//       selectAll: false,
//       selected: [],
//       headers: [
//         {
//           text: "PDF file",
//           align: "start",
//           sortable: false,
//           value: "name",
//         },
//         { text: "ID", value: "id" },
//       ],
//       documents: ["sdsada", "ASDasd"],
//     };
//   },
</script>


