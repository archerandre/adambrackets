NO PRESEASON BIAS (NPB) 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Written by: Professor of Ball Knowledge, Adam Davis - @adambrackets on social media, or "Ba11L0V3R". Call me what you want; I am alias fluid.  

For: Master of Nuclear Code, Andre Archer, @Andrearcher@gmail.com

This README will guide you through the columns of the NPB CALCULATION tab in each of my updated spreadsheets.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Theoretical nonsense: 
This is based on the idea that the data I am drawing from relies too heavily on its preseason assumptions for the early part of the year. This is literally admitted by Ken Pomeroy in a forum.  
NPB v1.0 was developed with a few key ideas involved: 
	1. The elimination of preseason bias early in the year provides for a more accurate depiction of a given team's power.
		1a. This preseason bias may fade as more data points are accounted for by torvik and kenpom, but ONLY for power conference teams, as mid majors who upset teams int the tournament are still too low. 
	2. The mentioned mid major bias (see 1.a) is because of their adjusted numbers in-conference being significantly lower; this mid major bias works fine for home/away regular season games, NOT tournament games.
	3. This is still experimental, but with automated calculation for all years we can try to fix any issues with a better model.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List of original calculations done in Spreadsheet:

1. Rating Difference (Column H)
2. Raw Improvement Index, "RII" (Column J)
3. Adjusted Improvement Index, "AII" (Column K)
4. True Performance Rating, "TPR" (Column M) - This is the "NPB rating" so maybe I should call it that. 

Other Stored Data (You can ignore these cells located off to the right while looking at the spreadsheet, I have written them straight into the formulas in the Typical Spreadsheet section):

1. AVG Rating Difference (Column R, Row 2)
2. Squared Avg Rating Difference (Column R, Row 3)
3. Maximum of Raw Improvement Index (Column S, Row 2)

Something of Note:
We are not using any of the rankings of the values to calculate the resultant True Performance Rating (NPB Rating), however I included a lot of cells that display each rank.
This is just so I could look at it while I was making it, and see what teams excelled in other places. I'm saying this because in RPPF we used the ranks as well as values to calculate which teams were excelling in certain areas, despite the inability to average the unitless numbers. Since RPPF and NPB are not actually calculated the same way, and the values are effectively unitless, this could be a way that NPB changes in the future to increase accuracy.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imported Data: 
1. PRESEASON RPPF VALUES
	1a. These are composed of Preseason Kenpom and Preseason Torvik. You cannot find the torvik preseason values past 2014-2015, and the values are not inclusive to all teams on the first day of the season like they are for kenpom.
	1b. See RPPF PRESEASON CALCULATION README for how to calculate the preseason numbers. For this year (2024-2025) I have provided you the numbers to get things rolling, and there is not a torvik link for 2024-2025 yet. 

2. CURRENT RPPF CALCULATION
	2a. Since you have created a working version of RPPF, you can use the resultant RPPF values in this NPB calculation.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NPB Typical Spreadsheet:

Column B: Preseason RPPF Value

Column C: Team Name
	- For visual convenience/Ease of Matching

Column D: Preseason RPPF Rank
	- For visual convenience

Column E: Team Name
	- For visual convenience/Ease of Matching

Column F: Current RPPF Value

Column G: Current RPPF Rank
	- For visual Convenience

Column H: Rating Difference
	Eqn. (names): Current RPPF - Preseason RPPF
	Eqn. (columns): Column F - Column B

Column I: Rank Difference
	- For visual convenience
	- Since the numerical value of rank is inverse to RPPF value, you reverse the subtraction
	Eqn. (names): Preseason RPPF Rank - Current RPPF Rank
	Eqn. (columns): Column D - Column G

Column J: Raw Improvement Index (RII)
	- We need the average rating difference of ALL teams for this one since it is more or less an ELO system. This is the TOTAL AVG of all values in column H (Rating Difference).
	- Notice that new negative sign in front of the rating difference
	Eqn. (names): Current RPPF Value - [-Rating Difference - AVG(Rating Difference Column)]
	Eqn. (columns): Column F- [-Column H - AVG(Column H)]

Column K: Adjusted Improvement Index (AII)
	- This just keeps the improvement from becoming too inflated so that the NPB and RPPF values both stay below 1. They aren't really interchangeable, as NPB is generally much higher than RPPF for all teams.
	- The maximum improvement of column J is to be found and then we can adjust by dividing by that max, as many improvement indexes will be greater than 1. 
	Eqn. (names):  Absolute Value[(Raw Improvement Index)/(Maximum of Improvement Index Column)]
	Eqn. (columns):  Absolute Value[(Column J)/(Max Column J)]

Column L: Team Name
	- For visual convenience

Column M: True Performance Rating (TPR) ---- AKA "NPB RATING"
	- This is the most complex part: You will multiply the current RPPF rating by the Square Root of the adjusted improvement index, and raise that result to the 1/2.5. Then subtract the squared avg rating difference.
	Eqn. (names): {[Current RPPF Value * Square Root(Adjusted Improvement Index)]}^(1/2.5) - {[AVG(Rating Difference Column)]}^2
	Eqn. (columns): {[Column F * Square Root(Column K)]^(1/2.5)} - {[AVG(Column H)]}^2

Column N: TPR Rank
	- For visual Convenience