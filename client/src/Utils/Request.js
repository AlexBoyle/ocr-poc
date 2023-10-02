import axios from "axios";

let Request = function () {
  this.get = function (route, handleSuccess, handleError, config) {
    axios
      .get(route, { ...config })
      .then((res) => {
        handleSuccess(res);
      })
      .catch((err) => {
        handleError(err);
      });
  };
  this.post = function (route, body, handleSuccess, handleError, config) {
    axios
      .post(route, body, { ...config })
      .then((res) => {
        handleSuccess(res);
      })
      .catch((err) => {
        handleError(err);
      });
  };
};
export default new Request();
