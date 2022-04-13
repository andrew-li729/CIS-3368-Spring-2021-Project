import CRUD as c
import flask
import myfunctions
import mysql.connector
import random

from mysql.connector import Error
from flask import Flask, request, jsonify, make_response, abort
from myfunctions import execute_query, execute_read_query, create_connection

if __name__ == '__main__':
    # creates connection to database
    connection = create_connection(
        "cis3368-database.cw8q49oufrn8.us-east-1.rds.amazonaws.com",  # RDS Endpoint
        "ali22",                                                      # username
        "Ep^63mC^If5!",                                               # password
        "FinalProject"                                                # DB name in mySQL workbench
        )

    # setting up an application name
    app = Flask(__name__) #set up application
    app.config["DEBUG"] = True #allow to show error message in browser

    @app.route('/', methods=['GET'])  #routing = mapping urls to functions; home is usually mapped to '/'
    def home():
        return "<h1>Welcome to my final project API!</h1>"
    
    # this url is mapped to display all values in the friend table
    @app.route('/api/friends/all', methods=['GET'])
    def friendsAll():
        cursor = connection.cursor(dictionary=True)
        # selects all records from friend table to display
        sql = "SELECT * FROM friend"
        cursor.execute(sql)
        rows = cursor.fetchall()
        results = []
        # result of query is iterated through to put each row into results list
        for friend in rows:
            results.append(friend)
        # list of rows in dict form are jsonified to be displayed on API page
        return jsonify(results)

    # this url us mapped to display all values in movielist table
    @app.route('/api/movies/all', methods=['GET'])
    # this function selects all movies in movielist
    def moviesAll():
        cursor = connection.cursor(dictionary=True)
        # functions similar to friendsAll() function, selects all movie records from movielist
        sql = "SELECT * FROM movielist"
        cursor.execute(sql)
        rows = cursor.fetchall()
        # result of query is iterated through to put each row into results list
        results = []
        for movielist in rows:
            results.append(movielist)
        # list of rows in dict form are jsonified to be displayed on API page
        return jsonify(results)

    # this url is mapped to select a random movie from within the moviestable
    @app.route('/api/movies/random', methods=['GET'])
    def moviesRandom():
        # blank movie list for scraped movies to be placed in
        movieList = []
        cursor = connection.cursor(dictionary = True)
        # gets columns names using functions from CRUD.py
        moviesColumns = c.getMovieCol(connection)
        # iterates by columns in movielist table and selects values where not null
        for col in moviesColumns:
            sql = "SELECT {0} FROM movielist WHERE {0} IS NOT NULL".format(col)
            cursor.execute(sql)
            movie = cursor.fetchall()
            # appends selected movie to movieList list
            movieList.append(movie)

        flatList = []
        # flattens list since raw movieList is list of list of dicts
        for sublist in movieList:
            for val in sublist:
                flatList.append(val)
        # usees random module to select a random movie from flattened movie list and is jsonified
        return jsonify(random.choice(flatList))

    # Adding a user to my database of users
    @app.route('/api/adduser', methods=['POST'])
    def adduser():
        if request.method=='POST':
            request_data = request.get_json()
            firstname = request_data['firstname']
            lastname = request_data['lastname']
        
            # now we just have to execute a query in our remote DB
            # conn = create_connection("cis3368.ch0zbpdqra6t.us-east-1.rds.amazonaws.com", "username", "password", "dbname")
            sql = "INSERT INTO friend (firstname, lastname) VALUES ('"+firstname+"','"+lastname+"')"
            myfunctions.execute_query(connection, sql)

            sql2 = "INSERT INTO movielist (friendid) VALUES (LAST_INSERT_ID())"  # uses LAST_INSERT_ID to get primary key from last inserterd record
            myfunctions.execute_query(connection, sql2)  
            return 'POST REQUEST WORKED'
            #check my table in mySQL Workbench to verify the user has been added

    # route to add movies to db
    @app.route('/api/addmovies', methods=['POST'])
    def addmovies():
        if request.method=='POST':
            # gets json data posted by node frontend form
            request_data = request.get_json()
            friendid = request_data['friendid']
            moviename = request_data['moviename']
            # function from CRUD.py used to add movies
            c.movieInput(connection, moviename, friendid)
            return 'POST REQUEST WORKED'

    # route to modify movies in db
    @app.route('/api/modifymovie', methods=['POST'])
    def modifymovie():
        if request.method=='POST':
            # like before, gets data from json posted by frontend form
            request_data = request.get_json()
            friendid = request_data['friendid']
            moviename = request_data['moviename']
            movieCol = request_data['movieCol']
            # function executed using data retrieved from front end
            c.movieUpdate(connection, movieCol, friendid, moviename)
            return 'POST REQUEST WORKED'       
    
    # route to delete movies from db, works functionally the same as previosuly explained routes
    @app.route('/api/deletemovie', methods=['POST'])
    def deletemovie():
        if request.method=='POST':
            request_data = request.get_json()
            movieCol = request_data['movieCol']
            friendid = request_data['friendid']
            c.movieDelete(connection, movieCol, friendid)
            return 'POST REQUEST WORKED'     

    # route to modify users from db, works functionally the same as previosuly explained routes
    @app.route('/api/modifyuser', methods=['POST'])
    def modifyuser():
        if request.method=='POST':
            request_data = request.get_json()
            friendid = request_data['friendid']
            firstname = request_data['firstname']
            lastname = request_data['lastname']
            c.updateFriend(connection, friendid, firstname, lastname)
            return 'POST REQUEST WORKED'

    # route to delete users from db, works functionally the same as previosuly explained routes
    @app.route('/api/deleteuser', methods=['POST'])
    def deleteuser():
        if request.method=='POST':
            request_data = request.get_json()
            friendid = request_data['friendid']
            c.deleteFriend(connection, friendid)
            return 'POST REQUEST WORKED'

    app.run()

    # for testing within python
    # movieList = []
    # cursor = connection.cursor(dictionary = True)
    # moviesColumns = c.getMovieCol(connection)
    # for col in moviesColumns:
    #     sql = "SELECT {0} FROM movielist WHERE {0} IS NOT NULL".format(col)
    #     cursor.execute(sql)
    #     movie = cursor.fetchall()
    #     movieList.append(movie)
    
    # flatList = []
    # for sublist in movieList:
    #     for val in sublist:
    #         # print(val)
    #         flatList.append(val)
    # print(random.choice(flatList))

    # print(movieList)
    # return jsonify(movieList)