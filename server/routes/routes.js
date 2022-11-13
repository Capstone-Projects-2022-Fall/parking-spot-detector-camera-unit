const userRoutes = require('./users');
const cameraRoutes = require('./camera');

const appRouter = (app, fs) => {

  app.get('/', (req, res) => {
    res.send('welcome to the development api-server');
  });

  userRoutes(app, fs);
  cameraRoutes(app, fs);
};

module.exports = appRouter;
