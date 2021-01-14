import http from "../http-common";
import axios from "axios"

class UploadFilesService {
  upload(file, onUploadProgress) {

    let formData = new FormData();
    for( let i = 0; i < file.length; i++ ){
        const filex = file[i];
        formData.append('files', filex);
    }

    return http.post('/upload', formData, {
      headers: {
        'Accept': "multipart/form-data",
        'Cache-Control': "no-cache",

      },    onUploadProgress

    }

    )

    // http://localhost:8000/PDF/uploadfiles
    // axios.post('http://localhost:1337/upload', formData, {
    //     headers: {
    //       'Accept': "multipart/form-data",
    //       'Cache-Control': "no-cache",

    //     },    onUploadProgress

    //   }
    // )
  }

  getFiles() {
    console.log("get files");
    return axios.get("http://localhost:1337/documents");
  }

 
}

export default new UploadFilesService();