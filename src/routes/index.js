const express = require("express");
const router = express.Router();
const homeController = require("../controllers/home");
const uploadController = require("../controllers/upload");
const trainController = require("../controllers/trainController");

let routes = app => {
  router.get("/", homeController.getHome);
  router.get("/uploadSuccess", homeController.getUploadSuccess);

  router.post("/upload", uploadController.uploadFiles);
  router.get("/files", uploadController.getListFiles);
  router.get("/files/:name", uploadController.download);

  router.post('/train', trainController.train);

  return app.use("/", router);
};

module.exports = routes;