RPPF PRESEASON CALCULATIONS

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Written by: Professor of Ball Knowledge, Adam Davis - @adambrackets on social media, or "Ba11L0V3R". Call me what you want; I am alias fluid.  

For: Master of Nuclear Code, Andre Archer, @Andrearcher@gmail.com

This README will guide you through the columns of the NPB CALCULATION tab in each of my updated spreadsheets.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imported Data:
	1. Kenpom Data for First Day of Season (Must get from Ratings Archive) https://kenpom.com/fanmatch.php?d={YEAR}-{MONTH}-{DAY}
	2. 


Torvik Preseason Scraper has been designed already; I included it in the email that you got this README from originally.

1st Days of Season (FOR Kenpom Archive)

(FOR 2014 - 2015): 2014-11-14 
(FOR 2015 - 2016): 2015-11-13
(FOR 2016 - 2017): 2016-11-11
(FOR 2017 - 2018): 2016-11-11
(FOR 2018 - 2019): 2017-11-10
(Skip 2019-2020 for now, there was no tournament.)
(FOR 2020 - 2021): 2020-11-25
(FOR 2021 - 2022): 2021-11-09
(FOR 2022 - 2023): 2022-11-07
(FOR 2023 - 2024): 2023-11-06

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RPPF PRESEASON Typical Spreadsheet: 
	
Column A-C: Filter logic. (CURRENTLY DOES NOT WORK) 
	(Placeholder val = 1; this currently does not change anything about the ratings. Eventually it will be a conference-based score, where larger conferences are weighted differently than mid majors to re adjusted adjEM numbers 	based on inflation. Inspiration: Gonzaga every year.)

Column D-G: Kenpom Data
	Column D is the original Team Name

Column H: Tempo-Relative Efficiency Margin (TREM)
	Eqn: (AdjOE - AdjDE)/RawTempo

Column I: TREM Rank
	Ranked from greatest to smallest value (smallest values are negative)

Column J: Tempo-Relative Offensive Efficiency (TROE)
	Eqn: (AdjOE^2)*Raw Tempo 

Column K: TROE Rank
	Ranked from greatest to smallest value (all positive)

Column L: Torvik A-N Barthag Approximation
	Eqn (names): 0.98 * Barthag 
	Eqn (columns): (0.98 * Column N)

Column M: Torvik A-N Barthag Approximation Rank

Column N: Torvik Preseason Barthag Value
	(Get Preseason Value; I made a script that you could incorporate)

Column O: AN&H Approximation (AVG of A-N and H Barthag Value)
	Eqn (names): (A-N Barthag Aprroximation + Preseason Barthag)/2
	Eqn (columns): (Column N + Column L)/2

Column P: RANK AVG of A-N and H Barthag Value

Column Q: Momentum Value Approximation
	Eqn. (names): 1.01 * A-N Barthag
	Eqn. (columns): 1.01 * Column L

Column R: Momentum Rank
	
Column S: Tovik Noncon Barthag Approximation
	Eqn. (names): 0.95 * (ANHBarthag)
	Eqn. (columns): 0.95 * Column O

Column T: Torvik Noncon Barthag Approximation Rank

Column U: AVG "BIG 5" Rank
	Formula (Columns): (Column I + Column K + Column P + Column R + Column T) / 5
	Formula (Names): (TPREM Rank + TROE Rank + A-N&H Rank + Momentum Rank + Noncon Rank) / 5

Column V: Champion Filter 
	Formula: (Columns): (Column U/Column L)
	Formula (Names): (AVG BIG 5 Rank / A-N Barthag Value)

Column W: Champion Filter Rank
	Ranked from smallest to greatest value

Column X: Power Filter
	Formula: (Columns): (Column U/Column N)
	Formula (Names): (AVG BIG 5 Rank / A-N + H AVG Barthag Value)

Column Y: Power Filter Rank
	Ranked from smallest to greatest value

Column Z: Team Name
	(column Z = column D)
	This is for visual convenience in spreadsheet.

Columnn AA: Davis Value 1
	Formula (Columns): (Column N * ((MIN(Column V))/Column V)^(1/10)))
	Formula (Names): Torvik A-N * (((MIN Rank of all Champ Filter)/(Champ Filter Rank))^(1/10))

Columnn AB: Davis Value 2
	Formula (Columns): (Column N * ((MIN(Column X))/Column X)^(1/10)))
	Formula (Names): Torvik A-N * (((MIN Rank of all Power Filter)/(Power Filter Rank))^(1/8))

Column AC: RPPF Rating
	Formula (Columns): ((Column AA + Column AB) / (2) )^(1/2.5)
	Fromula (Names): (((DV1 + DV2)) / (2))^(1/2.5)

Column AD: Team Name 
	(Column AD = Column Z = Column D)
	(for convenience)

Column AE: RPPF Rank
	Ranked from greatest to smallest decimal value

Column AF: Blank (So the spreadsheet looks better)

Column AG: Filter Labels

Column AH: Power Filter Minimum Reference
	(MIN(Column X))
	This is where I store the minimum for Power Filter. You can ignore it since I already put this into the above formulas.

Column AI: Champ Filter Minimum Reference
	(MIN(Column V))
	This is where I store the minimum for Champ Filter. You can ignore it since I already put this into the above formulas.
