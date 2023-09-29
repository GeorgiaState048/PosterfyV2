App.jsx will be responsible for obtianing the access_token. 
It will then post it to the endpoint that I make in app.py
    Token goes from front end -> back end

The endpoint that I make in app.py reads that access_token and sets it as a global variable, this way any of my back end components can use it. 
