//os
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

//server
const express = require('express');
const app = express();
const multer = require('multer');
const port = 8000;

//ip
const { networkInterfaces } = require('os');
function getIP() {
  const nets = networkInterfaces();
  let results='';

  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      // Skip over non-IPv4 and internal (i.e. 127.0.0.1) addresses
      // 'IPv4' is in Node <= 17, from 18 it's a number 4 or 6
      const familyV4Value = typeof net.family === 'string' ? 'IPv4' : 4
      if (net.family === familyV4Value && !net.internal) {
        if (!results[name]) {
          results[name] = [];
        }
        results[name].push(net.address);
      }
    }
  }

  try {
    results = results['Wi-Fi'][0];
  } catch (_) {
    results = 'ip_not_found';
  }

  return results;
}

//path and URL
const clientUrl = `http://localhost:${port}`;
const CONFIG_PATH = path.join(__dirname, '/src/config.json');
const configFile = require(CONFIG_PATH);
let launched = false;

//picture modificatin
const sharp = require('sharp');

const FORM_MAP = {
  tagline: {
    tagline_value: 'value',
    tagline_start: 'start',
    tagline_end: 'end',
    tagline_size: 'fontsize',
    tagline_video: 'video'
  },
  client: {
    client_start: 'start',
    client_end: 'end',
    client_size: 'size',
    client_video: 'video'
  }
}


app.use(express.json());
app.use(express.urlencoded({ extended: true }));

//---------------
console.log('Starting server...')
app.use(express.static(path.join(__dirname, '/public')));
app.listen(port);


const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, '/src/assets/'));
  },
  filename: function (req, file, cb) {
    const extension = file.originalname.split('.')[1];
    const filepath = file.fieldname + '.' + extension;
    cb(null, filepath);
  }
});

const upload = multer({ storage: storage });


console.log(`Server now available on: ${clientUrl}`);
console.log(`On local network: ${getIP()}`);

//start client
switch (process.platform) {

  case 'win32':
    exec(`start ${clientUrl}`);
    break;

  case 'darwin':
    exec(`open ${clientUrl}`);
    break;
}

function rescaleLogo(req, res) {
  console.log('\n2.Request Files:\n');
  if (!req.file) {
    console.log("No file received");
  } else {
    console.log('file received');
    if (req.file?.fieldname === 'client') {
      //resize picture
      const { width, height } = configFile.client;
      const { path } = req.file;
      console.log('Resizing logo...')
      sharp(path)
        .resize(parseInt(width), parseInt(height), { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
        .png()
        .toBuffer()
        .then(bf => {
          console.log(`Rescaled logo saved to: ${path}`);
          return sharp(bf).toFile(path);
        })
        .catch(er => console.log(er));
    }

  }
}


function onUpdate(req, res) {

  console.log('\n\n\n_____________________________________');
  console.log('_______________UPDATES_______________');
  console.log('_____________________________________');

  console.log('\n1.Request Body:\n');

  Object.keys(req.body).map(item => {

    const value = req.body[item];
    const parentKey = item.split('_')[0];
    if (!FORM_MAP[parentKey]) { return; }

    const childKey = FORM_MAP[parentKey][item];

    console.log({ parentKey, childKey, value });

    if (value && value.length && configFile[parentKey][childKey]) {
      console.log(`${configFile[parentKey][childKey]} => ${value}`);
      configFile[parentKey][childKey] = value;
    }

  });

  fs.writeFile(CONFIG_PATH, JSON.stringify(configFile, null, 2), function writeJSON(err) {
    if (err) return console.log(err);
    //console.log(configFile);
    console.log('=> Writing to ' + CONFIG_PATH);
    console.log('\n\n');
  });

  rescaleLogo(req, res);

}

function onLaunch(req, res) {

  if (launched) { return res.send({ success: false }); }
  launched = true;

  let setup = "\"" + (path.join(__dirname, configFile.applications.setup)) + "\"";
  console.log(setup);
  if (process.platform === 'win32') { //reverse slash for windows
    //setup = setup.substring(2);
    setup = setup.replaceAll('/', '\\');
  }


  console.log('=> Lauching: ' + setup);
  exec(`python ${setup} ${__dirname}`, (err, stdout, stderr) => console.log({ err, stdout, stderr }));

  setTimeout(() => exec('taskkill /f /im chrome.exe'), 9000);

  rescaleLogo(req, res);

  return res.send({ success: true });

}


app.post('/', upload.single('client'), function (req, res) {


  const { action } = req.body;


  switch (action) {

    case 'update':
      onUpdate(req, res);
      break;

    case 'launch':
      onLaunch(req, res);
      break;

    default:
  }


  console.log('\n\n');
  console.log('_____________________________________');


});


app.post('/getConfig', (req, res) => {
  res.send(JSON.stringify(configFile));
});

app.post('/getIP', (req, res) => res.send({ ip: getIP() }));
