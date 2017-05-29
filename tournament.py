#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete FROM Matches;")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete FROM Players;")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("select count(*) from Players;")
    p = int(c.fetchone()[0])
    DB.commit()
    DB.close()
    return p


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert INTO Players(player_name) VALUES (%s);",(name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""select standings.player_id, standings.player_name, standings.wins,
    standingsAll.total_matches from standings,standingsAll where
    standings.player_id = standingsAll.player_id ORDER BY wins desc;""")
    standing = []
    for s in c.fetchall():
    	standing.append(s)
    DB.commit()
    DB.close()
    return standing


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""insert INTO Matches(winner_id,looser_id) VALUES (%s,%s)"""
    	,(winner, loser,))
    DB.commit()
    DB.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    c.execute("select * from standings;")
    x = c.fetchall()
    DB.commit()
    DB.close()
    result = []
    i = 0
    while  i < len(x):
    	A_id = x[i][0]
    	A_name = x[i][1]
    	B_id = x[i+1][0]
    	B_name = x[i+1][1]
    	result.append(A_id,A_name,B_id,B_name)
    	i += 2
    return result


