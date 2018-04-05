# Command line NBA
Command line NBA scores and stats written in Python3

Using the data.nba.net endpoint.

Dates have been adjusted for users in the Australian timezone (me), as 'today' here is 'yesterday' in the US.

I will add more functionality as I find time to do so.

## Usage

For ease of use, i've added the following to my ~/.bash_profile file:
`alias nba="python3 ~/whateverdirectory/nba.py"`

Type `nba` into command line to get scores

Type `s` to see scores again, or type the game number to get the box score for that game

To quit, type `cmd+d` (standard EOF input)
