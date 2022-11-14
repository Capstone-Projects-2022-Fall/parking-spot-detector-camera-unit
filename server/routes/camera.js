const cameraRoutes = (app, fs) => {
  // variables
  const dataPath = './data/users.json';

  // READ
  app.get('/get_current_frame', (req, res) => {
    fs.readFile(dataPath, 'utf8', (err, data) => {
      if (err) {
        throw err;
      }

      res.send(JSON.parse(data));
    });
  });

  app.post('/set_mask', (req, res) => {

  });
};

module.exports = cameraRoutes;
