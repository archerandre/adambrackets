RELATIVE POWER AND PERFORMANCE FILTER (RPPF) 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Written by: Professor of Ball Knowledge, Adam Davis - @adambrackets on social media

This README will guide you through the columns of the VALUES tab in each of my spreadsheets.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Theoretical nonsense: 
This was first theorized based on the creation of a tournament-first approach to rating basketball teams. 
The inner-workings have been developed with a few key ideas involved: 
	1. Teams can be rated in a relative manner based on the BEST team rather than the average team.
	2. Greater away/neutral site games are indicative of successful tournament teams.
	3. Teams may be filtered based on their level of play against weaker teams that may inflate or depreciate their adjusted metrics (mid major vs power conference).
		- This third thing isn't done yet. Filter logic is just set up to be "inclusive." AKA all teams are rated the same (not ideal). 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List of original calculations done in Spreadsheet:

1. TREM (Column S)
2. TROE (Column U)
3. Champion Filter (Column AG)
4. Power Filter (Column AI)
5. Davis Value 1 (Column AM)
6. Davis Value 2 (Column AN)
7. RPPF Rating (Column AO)
8. Sweet 16 Index (Column AS)
9. Index Rank (Column AT)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imported Data: 
1. Kenpom Pre-Tournament Data (Column D-R)
2. Torvik Data
	2.a A-N (ALL; 11-01 to Day After Selection Sunday)
	2.b H (ALL; 11-01 to Day After Selection Sunday)
	2.c Momentum (A-N; 1-31 to Day After Selection Sunday)
	2.d NonCon (Noncon - ALL; 11-01 to Day After Selection Sunday - Most Nonconference play ends on Dec 31st, but some home and home series exist in the new year.)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RPPF Typical Spreadsheet: 
	
Column A-C: Filter logic. (CURRENTLY DOES NOT WORK) 
	(Placeholder val = 1; this currently does not change anything about the ratings. Eventually it will be a conference-based score, where larger conferences are weighted differently than mid majors to re adjusted adjEM numbers 	based on inflation. Inspiration: Gonzaga every year.)

Column D-R: Kenpom Data
	Column D is the original Team Name

Column S: Tempo-Relative Efficiency Margin (TREM)
	Eqn: (AdjOE - AdjDE)/RawTempo

Column T: TREM Rank
	Ranked from greatest to smallest value (smallest values are negative)

Column U: Tempo-Relative Offensive Efficiency (TROE)
	Eqn: (AdjOE^2)*Raw Tempo 

Column V: TROE Rank
	Ranked from greatest to smallest value (all positive)

Column W: Torvik A-N Barthag Value
	(A-N; 11-01 to Day After Selection Sunday)

Column X: Torvik A-N Barthag Rank

Column Y: Torvik H Barthag Value
	(ALL; 11-01 to Day After Selection Sunday)

Column Z: AN&H (AVG of A-N and H Barthag Value)
	Eqn: (A-N Barthag + H Barthag)/2

Column AA: RANK AVG of A-N and H Barthag Value

Column AB: Momentum Value
	Torvik A-N Barthag; 1-31 to Day After Selection Sunday

Column AC: Momentum Rank
	(A-N; 1-31 to Day After Selection Sunday)

Column AD: Tovik Noncon All Barthag Value
	(ALL; 11-01 to Day After Selection Sunday - Most Noncon ends on Dec 31st, but some home and home series exist in the new year.)

Column AE: Torvik Noncon All Barthag Rank

Column AF: AVG "BIG 5" Rank
	Formula (Columns): (Column T + Column V + Column AA + Column AC + Column AE) / 5
	Formula (Names): (TPREM Rank + TROE Rank + A-N&H Rank + Momentum Rank + Noncon Rank) / 5

Column AG: Champion Filter 
	Formula: (Columns): (Column AF/Column W)
	Formula (Names): (AVG BIG 5 Rank / A-N Barthag Value)

Column AH: Champion Filter Rank
	Ranked from smallest to greatest value

Column AI: Power Filter
	Formula: (Columns): (Column AF/Column Z)
	Formula (Names): (AVG BIG 5 Rank / A-N + H AVG Barthag Value)

Column AJ: Power Filter Rank
	Ranked from smallest to greatest value

Column AK: Top Rank
	Minimum rank of a team in any area (Not factored into ratings; this is just a visual on what teams have excelled in at least one area so far.)

Column AL: Team Name
	(column AL = column D)
	This is for visual convenience in spreadsheet.

Columnn AM: Davis Value 1
	Formula (Columns): (Column W * ((MIN(Column AG))/Column AG)^(1/10)))
	Formula (Names): Torvik A-N * (((MIN Rank of all Champ Filter)/(Champ Filter Rank))^(1/10))

Columnn AN: Davis Value 2
	Formula (Columns): (Column W * ((MIN(Column AI))/Column AI)^(1/10)))
	Formula (Names): Torvik A-N * (((MIN Rank of all Power Filter)/(Power Filter Rank))^(1/8))

Column AO: RPPF Rating
	Formula (Columns): ((Column AM + Column AN) / (2) )^(1/2.5)
	Fromula (Names): (((DV1 + DV2)) / (2))^(1/2.5)

Column AP: Team Name 
	(Column AP = Column AL = Column D)
	(for convenience)

Column AR: RPPF Rank
	Ranked from greatest to smallest decimal value

Column AS: Sweet 16 Index
	Formula (Columns): If ((RANK(Column W) OR RANK(Column Y)) <17), = Y, else = ""
	Formula (Names): If (Rank(A-N)) OR (Rank(H)) <17, = Y, else ""

Column AT: Index Rank
	1. SORT Column AR Smallest to Largest
	2. SORT Column AS Z to A
	3. Apply new ranking as listed.

Column AU: Blank (So the spreadsheet looks better)

Column AV: Filter/Min Labeling/Color Key

Column AW: Power Filter Minimum Reference
	(MIN(Column AG)
	This is where I store the minimum for Power Filter.

Column AX: Champ Filter Minimum Reference
	(MIN(Column AI))
	This is where I store the minimum for Champ Filter.


	
