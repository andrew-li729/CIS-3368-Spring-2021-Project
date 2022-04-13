import datetime
from flask import Flask, request, jsonify
import myfunctions
import mysql.connector
from myfunctions import create_connection, execute_query, execute_read_query
from mysql.connector import Error

# DB Password: Ep^63mC^If5!
# !!NOTE!! Renamed file and committed but lost all previous commits unknowningly

# CRUD operations for friend and movielist tables
# CREATE
def addFriend(connection):
    # takes user input for friend name to be input
    firstName = input("Enter friend's first name: ")
    lastName = input("Enter friend's last name: ")
    sql = "INSERT INTO friend (firstname, lastname) VALUES ('%s', '%s')" % (firstName, lastName)
    connection = connection
    execute_query(connection, sql)

    # inserts friendid from newly added record in friend table to friendid column in movielist table, creating a new record based on that friendid
    sql2 = "INSERT INTO movielist (friendid) VALUES (LAST_INSERT_ID())"  # uses LAST_INSERT_ID to get primary key from last inserterd record
    execute_query(connection, sql2)

# READ
# reads and prints contents of friend table
def readFriend(connection):
    connection = connection
    sql = "SELECT * FROM friend"
    friend = execute_read_query(connection, sql)
    for x in friend:
        print(x)
    print("\n")

# UPDATE
# updates records within friend table
def updateFriend(connection, friendid, firstname, lastname):
    
    # query to display the record that is about to be updated
    sql = "SELECT * FROM friend WHERE friendid = %s" % (friendid)
    users = execute_read_query(connection, sql)
    
    # if the query returns a blank record, do not allow for changes to be made
    if not users:
        print("No record with such ID found.")
    else:
        print("Record to be updated: ", users)
        updQuery = "UPDATE friend SET firstname = '%s', lastname = '%s' WHERE friendid = %s" % (firstname, lastname, friendid)
        execute_query(connection, updQuery)

# DELETE
# deletes records based on friendID of record to be deleted
def deleteFriend(connection, deleteID):
    sql = "DELETE FROM friend WHERE friendid = '%s'" % deleteID
    execute_query(connection, sql)
    # also deletes relevant record in movielist table using friendid
    sql2 = "DELETE FROM movielist WHERE friendid = '%s'" % deleteID
    execute_query(connection, sql2)

def getMovieCol(connection):
    connection = connection
    # this query selects all columns in movielist table that begin with "movie"
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'movielist' AND COLUMN_NAME LIKE 'movie%'"
    columns = execute_read_query(connection, query)
    movieColumns = []
    for col in columns:
        # results from query are placed into movieColumns list
        movieColumns.append(col[0])
    # print(movieColumns)
    # returns list of column names
    return movieColumns

# for adding movies for each friend in movielist table, adds movie to record if there are fields available 
def movieInput(connection, moviename, friendID):
    connection = connection
    
    cursor = connection.cursor()
    # calls getMovieCol() function to get names of columns
    movieColumns = getMovieCol(connection)
    # initiates count variable used to track if records were changed using cursor.rowcount
    count = 0

    # iterates through movieColumns list to check if column is filled for specified row
    for col in movieColumns:
        movieNumber = col
        # if column is NULL, update with user specified movie value
        sql = "UPDATE movielist SET {0}=IF({0} IS NULL, '{2}', {0}) WHERE friendid = '{1}'".format(movieNumber, friendID, moviename)
        cursor.execute(sql)
        connection.commit()
        # checks if changes were made to row after execeuting update query. Value = 0 if no, = 1 if yes
        count = cursor.rowcount
        # print(count)
        # if record was updated (count = 1), breaks for loop, stops looking for empty column
        if count == 1:
            print("Movie added!")
            break
        # if record was not updated (count = 0), continue on to next column 
        else:
            continue
    # this condition is only reached if previous for loop does not find an empty column meaning no records were changed, count remains equal to 0
    if count == 0:
        print("Movie list full!")

# updates records in movielist table based on movie column and friend ID
def movieUpdate(connection,movieCol,friendID,movieName):
    connection = connection
    
    sql = "UPDATE movielist SET {0}=IF({0} IS NOT NULL, '{2}', {0}) WHERE friendid = '{1}'".format("movie"+str(movieCol), friendID, movieName)
    execute_query(connection, sql)

# deletes records in movielist table column name and friend ID
def movieDelete(connection, movieCol, deleteID):
    connection = connection
    sql = "UPDATE movielist SET {col} = NULL WHERE (friendid = '{friendid}')".format(col = "movie"+str(movieCol), friendid = deleteID)
    execute_query(connection, sql)



if __name__ == '__main__':
    # creates connection to database
    connection = create_connection(
        "cis3368-database.cw8q49oufrn8.us-east-1.rds.amazonaws.com",  # RDS Endpoint
        "ali22",                                                      # username
        "Ep^63mC^If5!",                                               # password
        "FinalProject"                                                # DB name in mySQL workbench
        )
    
    # friend table CRUD operations to be executed
    # uncomment relevant function to test

    readFriend(connection)
    # getMovieCol(connection)
    # addFriend(connection)
    # updateFriend(connection)
    # deleteFriend(connection)
    # movieInput(connection)
    # movieUpdate(connection)
    # movieDelete(connection)