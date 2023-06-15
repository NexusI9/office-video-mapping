//os
const {exec} = require('child_process');
const fs = require('fs');

//server
const express = require('express');
const app = express();
const port = 8000; 

//path and URL
const clientUrl = `http://localhost:${port}`;
const configPath = __dirname + '/src/config.json';
const config = require(configPath);
let launched = false;

const formMap = {
  tagline:{
    tagline_value: 'value',
    tagline_start:'start',
    tagline_end:'end',
    tagline_size: 'fontsize',
    tagline_video:'video'
  },
  client:{
    client_start:'start',
    client_end:'end',
    client_size:'size',
    client_video:'video'
  }
}

//picture modificatin
const sharp = require('sharp');

//---------------
console.log('starting...')
app.use(express.static(__dirname + '/public'));
app.listen(port);

app.use(express.json());
app.use(express.urlencoded({extended: true}));


const multer = require('multer');
const storage = multer.diskStorage({
    destination: function(req, file, cb) {
      cb(null, __dirname + '/src/assets/' );
    },
    filename: function (req, file, cb) {
      const extension = file.originalname.split('.')[1];
      const filepath = file.fieldname+'.'+extension;
      cb(null, filepath);
    }
});

const upload = multer({storage: storage});
const configFile = require(configPath);

console.log(`Server available on: ${clientUrl}`);

//start client
switch(process.platform){

    case 'win32':
        exec(`start ${clientUrl}`);
    break;

    case 'darwin':
        exec(`open ${clientUrl}`);
    break;
}

app.post('/launch', function(req,res){

  console.log('launch');
  if(launched){ return res.send({success: false}); }
  launched = true;

  let setup = "\""+(__dirname + configFile.applications.setup).substring(2)+"\"";

  if(process.platform === 'win32'){ //reverse slash for windows
    setup = setup.replaceAll('/','\\');
  }

  console.log('=> Lauching: ' + setup );
  exec(`python ${setup} ${__dirname}`, (err, stdout, stderr) => console.log({err, stdout, stderr}) );

  setTimeout( () => exec('taskkill /f /im chrome.exe'), 9000);
  //setTimeout( () => exec('taskkill /f /im node.exe'), 10000);

  return res.send({success: true});

});

app.post('/', upload.single('client'), function(req, res){

    console.log(req.body);
    console.log('\n\n\n_____________________________________');
    console.log('_______________UPDATES_______________');
    console.log('_____________________________________');
    
    console.log('\n1.Request Body:\n');

    console.log('\n\n');
    //handle tagline
    Object.keys(req.body).map( item => {
      
      const value = req.body[item];
      const parentKey = item.split('_')[0];
      const childKey = formMap[parentKey][item];

      console.log({parentKey, childKey, value});

      if(value && value.length && configFile[parentKey][childKey] ){
        console.log(`${ configFile[parentKey][childKey]  } => ${value}`);
        configFile[parentKey][childKey] = value;
      }

    });

    fs.writeFile(configPath, JSON.stringify(configFile, null, 2), function writeJSON(err) {
        if (err) return console.log(err);
        console.log(configFile);
        console.log('=> Writing to ' + configPath);
        console.log('\n\n');
      });
      

    //handle picture
    console.log('\n2.Request Files:\n');
    if (!req.file) {
        console.log("No file received");
        res.send({ file: false });
      } else {
        console.log('file received');
        res.send({file: true });
        if(req.file?.fieldname === 'client'){
          //resize picture
          const {width, height} = config.client;
          const { path } = req.file;
          console.log(config.client);
          sharp(path)
            .resize(parseInt(width), parseInt(height), { fit: 'contain', background:{r:0, g:0, b:0, alpha:0} })
            .toBuffer()
            .then( bf => sharp(bf).toFile(path) );

        }
    
      }
    console.log('\n\n');

      console.log('_____________________________________');
      

});


app.post('/getConfig', (req,res)=>{ 
  res.send(JSON.stringify(configFile));
});
