const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const path = require('path');
// app.use(express.static(path.join(__dirname, 'console')));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));

// ------ Database ------
const mongoose = require('mongoose');
mongoose.connect(
  'mongodb://localhost:27017/data',
  { useNewUrlParser: true,
    useUnifiedTopology: true },
  (error) => {
    if (error) {
      console.error('Error during MongoDB connection:', error.message); // eslint-disable-line
      process.exit(1);
    }
  },
);

// ------ Enable cross origin requests
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'DELETE, PUT, GET, POST, OPTION');
  next();
});
app.listen(3000, () => {
  console.log('Connect localhost listening on port ' + 3000); // eslint-disable-line
});
app.use('/api', require('./routes/api'));