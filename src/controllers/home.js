const path = require("path");

const home = (req, res) => {
  return res.sendFile(path.join(`${__dirname}/../views/index.html`));
};

const getUploadSuccess = (req, res) => {
  return res.sendFile(path.join(`${__dirname}/../views/uploadSuccess.html`));
};

module.exports = {
  getHome: home,
  getUploadSuccess,
};
