# NBA Player Salary Efficiency Analysis

Goal
I wanted to find out which NBA players are giving teams the most value for their salary — basically, who's producing a lot on the court while getting paid relatively little, and who's getting paid a lot but not producing as much.

Code
nba_salary_efficiency.py

Description
I pulled live 2024-25 season stats for 569 players using the nba_api library, then merged that with a separate salary dataset I found on Kaggle since the stats API doesn't include contract info. I built a simple "production score" that combines points, rebounds, assists, steals, and blocks (weighting steals and blocks a bit higher since they're rarer), then divided that by each player's salary to get a value I called production per $1M.

One thing I ran into: players on minimum contracts (like $12,000 two-way deals) were showing up as the "most efficient" players just because their salary was so tiny, not because they were actually good. To fix this without deleting real data, I added a column that flags whether someone is a "rotation player" (played 40+ games, 15+ minutes per game, and earns at least $2M) so I could filter that noise out in the dashboard instead of hardcoding a cutoff in the data itself.

Skills used
Pulling data from an API, cleaning and merging two datasets that didn't line up perfectly (different name formats, missing matches), removing duplicate rows I found during the merge, building a custom metric, and designing a dashboard where the viewer can filter between "all players" and "real rotation players."

Tools
Python (pandas, numpy, nba_api), Power BI

What I found
About 89% of players matched between the stats and salary files. After filtering to real rotation players, guys like Andrew Nembhard, Walker Kessler, and Scotty Pippen Jr. came out on top for value. Interestingly, superstars like Stephen Curry showed up as "overpaid" by this metric — which makes sense once you think about it, since no amount of production can really keep up with a $55M salary. That's not a flaw in the data, just a limit of what this specific ratio is good for. It's better at spotting undervalued role players than judging superstars.

Dashboard includes
- Bar chart of the 10 most cost-efficient rotation players
- Bar chart of the 10 least efficient (most "overpaid") players
- Scatter plot showing all 467 matched players, salary vs. production, colored by whether they're a rotation player

What I'd improve with more time
I'd exclude max-contract superstars from the "overpaid" list since they're not a fair comparison, and try a more established stat like Win Shares instead of my own custom formula.
