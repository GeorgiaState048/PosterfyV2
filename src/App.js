import logo from './logo.svg';
import './App.css';
import env from 'react-dotenv';
// import { URLSearchParams } from 'url';
//import cors from "cors";

const express = require('express');
//const querystring = require('querystring');
const cors = require('cors');
const cookieParser = require('cookie-parser');

const client_id = 'ed53539aada74be99f89ffb57354241f';
const client_secret = '68c9e67dafb9421b8f63e37718e0a9ba';
const redirect_uri = 'http://127.0.0.1:5000/';
// Figure out how to use env variables with react (do not push the client secret or id to github)

const generateRandomString = function (length) {
  let text = '';
  const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (let i = 0; i < length; i += 1) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  } 
  return text; 
}

let stateKey = 'spotify_auth_state';

const app = express();
app.use(express.static(__dirname + '/public'))
    .use(cors())
    .use(cookieParser());

app.get('/login', function (req, res) {
  let state = generateRandomString(16);
  res.cookie(stateKey, state);

  const scope = 'user-read-private user-read-email';
  res.redirect('https://accounts.spotify.com/authorize?' +
    URLSearchParams.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state,
    }));
});

app.get('/callback', function (req, res) {
  let code = req.query.code || null;
  let state = req.query.state || null;
  let storedState = req.cookies ? req.cookies[stateKey] : null;

  if (state === null || state !== storedState) {
    res.redirect('/#' +
      URLSearchParams.stringify({
        error: 'state_mismatch'
      }));
  } else {
    res.clearCookie(stateKey);

    const authOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64'),
      },
      body: 'code=${code}&redirect_uri=${redirect_uri}&grant_type=authorization_code',
      json: true
    };

    fetch('https://accounts.spotify.com/api/token', authOptions)
      .then(response => {
        if(response.status === 200) {
          response.json().then((data) => {
            let access_token = data.access_token;
            let refresh_token = data.refresh_token;
            res.redirect('/#' +
              URLSearchParams.stringify({
                access_token: access_token,
                refresh_token: refresh_token
              }));
        });
      } else {
        res.redirect('/#' +
          URLSearchParams.stringify({
            error: 'invalid_token'
          }));
      };
    });
  };
});

app.get('/refresh_token', function (req, res) {
  const refresh_token = req.query.refresh_token;
  const authOptions = {
    method: 'POST',
    headers: {
      'Authorization': 'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64'),
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'grant_type=refresh_token&refresh_token=${refresh_token}',
  };
  fetch('https://accounts.spotify.com/api/token', authOptions)
  .then(response => {
    if(response.status === 200) {
      response.json().then((data) => {
        let access_token = data.access_token;
        res.send({'access_token': access_token});
      });
    };
  })
  .catch (error => {
    console.log(error);
    res.send(error);
  });
});

console.log('Listening on 5000');
app.listen(5000);

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>Boiiiii</code> and save to reload.
        </p>
        <a href="home">Home</a>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
