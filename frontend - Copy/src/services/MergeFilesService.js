import http from "../http-common";

class MergeFileService {
  // merge(file) {
  //   let formData = new FormData();
  //   for( let i = 0; i < file.length; i++ ){
  //       const filex = file[i];
  //       formData.append('files', filex);
  //   }
  //   return http.post("/PDF/merge", formData, {
  //     headers: {
  //       "Content-Type": "multipart/form-data"
  //     },

  //   });

  // }

  merge(selected) {
    console.log(selected);
    // let formData = new FormData();
    // for( let i = 0; i < file.length; i++ ){
    //     const filex = file[i];
    //     formData.append('files', filex);
    // }
    return http.post("/PDF/merge", selected, {
      headers: {
        "Content-Type": "multipart/form-data"
      },

    });

  }

  getFiles() {
    return http.get("/files");
  }
}

export default new MergeFileService();