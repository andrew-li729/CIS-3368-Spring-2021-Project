// load the things we need
var express = require('express');
var bodyParser = require('body-parser')
var app = express();

// middleman to parse form data from index page
var urlencodedParser = bodyParser.urlencoded({ extended: false })

// required module to make calls to a REST API
const axios = require('axios');
const { response } = require('express');

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// index page
app.get('/', function(req, res) {
    res.render('pages/home');
});





// USER ADD/MODIFY ROUTES
// renders add user page initially
app.get('/adduser', function(req, res) {
    res.render('pages/adduser')
});

// posts to adduser api path for api to execute Create operation
app.post('/adduser', urlencodedParser, function(req, res) {
    console.log(req.body.firstname)
    console.log(req.body.lastname)
    var firstname = req.body.firstname
    var lastname = req.body.lastname
    // axios post using firstname and lastname from forms
    axios.post('http://127.0.0.1:5000/api/adduser', {
        firstname:firstname,
        lastname:lastname
    });
    // renders confirmation page once form is submitted
    res.render('pages/userconfirm', {

    })
});

// renders initial modifyuser page and gets data from friends api endpoint to send to dropdown menu in form
app.get('/modifyuser', function(req, res) {
    axios.get('http://127.0.0.1:5000/api/friends/all')
        .then((response)=> {
            var friends = response.data;
            res.render('pages/modifyuser', {
                friends:friends
            });
        });
});

// posts to modifyuser api endpoint using data submitted from form
app.post('/modifyuser', urlencodedParser, function(req, res) {
    console.log(req.body.friendid)
    console.log(req.body.firstname)
    console.log(req.body.lastname)
    // creates variables from form data
    var friendid = req.body.friendid
    var firstname = req.body.firstname
    var lastname = req.body.lastname

    // axios post to execute crud operation
    axios.post('http://127.0.0.1:5000/api/modifyuser', {
        friendid:friendid,
        firstname:firstname,
        lastname:lastname
    });
    // renders confirmation page after form submission
    res.render('pages/modifyuserconfirm');
});

// posts selected friendid to delete from form to deleteuser endpoint to execute delete operation 
app.post('/deleteuser', urlencodedParser, function(req, res) {
    console.log(req.body.friendid)

    var friendid = req.body.friendid

    axios.post('http://127.0.0.1:5000/api/deleteuser', {
        friendid:friendid,
    });
    res.render('pages/modifyuserconfirm');
});




// MOVIES ADD/MODIFY ROUTES

// renders initial add movies page and populates dropdown with data from api
app.get('/addmovies', function(req, res) {
    axios.get(`http://127.0.0.1:5000/api/friends/all`)
        .then((response) => {
            // puts api response into var named friends
            var friends = response.data;
            // console.log(friends)

            // use res.render to load up an ejs view file
            res.render('pages/addmovies', {
                friends: friends,
            });
        });
});

// posts form data to addmovies api route to execute add movies query 
app.post('/addmovies', urlencodedParser, function(req, res) {
    console.log(req.body.friendid)
    console.log(req.body.moviename)
    var friendid = req.body.friendid
    var moviename = req.body.moviename
    axios.post('http://127.0.0.1:5000/api/addmovies', {
        friendid:friendid,
        moviename:moviename
        
    });
    res.render('pages/movieconfirm');
});

// renders initial modify movie page
app.get('/modifymovie', function(req, res) {
    axios.get('http://127.0.0.1:5000/api/friends/all')
        .then((response)=> {
            var friends = response.data;
            res.render('pages/modifymovie', {
                friends:friends
            });
        });
});

// posts form data to addmovies api route to execute modify movie query 
app.post('/modifymovie', urlencodedParser, function(req, res) {
    console.log(req.body.friendid)
    console.log(req.body.moviecol)
    console.log(req.body.moviename)

    var friendid = req.body.friendid
    var moviecol = req.body.moviecol
    var moviename = req.body.moviename

    axios.post('http://127.0.0.1:5000/api/modifymovie', {
        friendid:friendid,
        movieCol:moviecol,
        moviename:moviename
    });
    res.render('pages/modifymovieconfirm');
});

// posts form data to addmovies api route to execute delete movies query 
app.post('/deletemovie', urlencodedParser, function(req, res) {
    console.log(req.body.friendid)

    var moviecol = req.body.moviecol
    var friendid = req.body.friendid

    axios.post('http://127.0.0.1:5000/api/deletemovie', {
        friendid:friendid,
        movieCol:moviecol
    });
    res.render('pages/modifymovieconfirm');
});




// SELECT RANDOM MOVIE ROUTE
// renders page that has random movie selected from api response
app.get('/random', function(req, res){ 
    axios.get('http://127.0.0.1:5000/api/movies/random')
        .then((response)=>{
            // console.log(response.data)
            var obj = response.data
            var movie_choice = Object.keys(obj).map(function (key){ return obj[key];});
            console.log(movie_choice)
            res.render('pages/random', {
                movie_choice:movie_choice
            })
        })
});


app.listen(8080);
console.log('8080 is the magic port');