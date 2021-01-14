import http from "../http-common";
import axios from "axios";

class EditFilesService {

  get(id) {
    return http.get(`/PDF/${id}`);
  }

  create(data) {
    return http.post("/PDF", data);
  }

  update() {

    // let formData = new FormData();
    // for( let i = 0; i < prefixPage.length; i++ ){
    //     const pre = prefixPage[i];
    //     formData.append('files', filex);
    // }
    // return axios.put(`http://localhost:1337/documents/${id}`, );
  }

  delete(id) {
    return axios.delete(`http://localhost:1337/documents/${id}`);
  }

  deleteAll() {
    return http.delete(`/PDFs`);
  }

  findByTitle(title) {
    return http.get(`/PDF/?title=${title}`);
  }
}

export default new EditFilesService();
