Kyle Shannon - Udacity D3.js visual project
8/5/16
README.md file with 4 section

### Summary
[Summary] - in no more than 4 sentences, briefly introduce your data visualization and add any context that can help readers understand it

My visualization looks at a Major League Baseball data set and identifies some trends that have to do with handedness, e.g. left vs right hand. It is important to note that the MLB has a higher number of lefties and ambidextrous batters than the general population. There is a significant amount of players with zero home runs and a zero (0.000) batting average, these are most likely American League Pitchers. The visuals and data summary seem to suggest that there is def a difference in performance between lefties and righties in the MLB, this follows conventional wisdom and matches up with what other sources have reported on the issue.

### Design
[Design] - explain any design choices you made including changes to the visualization after collecting feedback

I wanted to implement a bar chart and scatter plot in my visual. I set out to use a bar chart, though probably verbose, to show the number of players grouped by handedness. A bar chart is good to show counted data which is grouped by categories, in the case handedness. I also added the percentage each group makes up of the total to the tool tip as another peice of information in the visual.  

A scatter plot was a perfect opportunity to look at relationships between Home runs and batting average. I wanted to see if there was a general trend between HRs and batting average, but I also wanted to segment the data by handedness. Using a scatterplot with different colored data would allow me to look at the data's relathionship while maintaining seperate groups. An interesting find was that almost no lefties dropped below the .200 batting average. Some feedback I received suggested that I make the scatterplot more interactive and either include an alpha for the individual points, or allow the user to hide data based on handedness. I decided to include an interaction that allowed a user to hide data. This made it easier to reveal the true scatter plot shape for each handedness group.

Another change I made was to add tables with summary statistics to show how each handedness compared to each other with respect to one dimension of data. This was good, because the scatterplot does not do the best job showing that lefties were more likely to have more home runs and better batting averages. This was a good suggestion.

Finally, a really good suggestion that I should have caught was the color difference between both the scatter plot and bar chart. That was a simple 3 liner fix with: e.g.: chart.assignColor("Right Handed","#fb8072"); This one was kinda strange, because the color was corect at time and other times the bar chart upon reloading chnaged color order, but setting it to those colors, which I found using inspect element on the bar charts, forced them everytime now to be the order I want.

### Feedback
[Feedback] - include all feedback you received from others on your visualization from the first sketch to the final visualization. The feedback are listed below:


#### Feedback 1:

1. Q: What do you notice in the visualization? A:There is a bar chart with some cool hover over effects/ dash line. Right handed players do make up a large majority of players, it seems like left handers make up quite a bit too, which is explained below the chart. The scatter plot seems a bit packed.
2. Q: What questions do you have about the data? A:I wonder how many people are being overlapped in the zero position of the scatter plot? 
3. Q: What relationships do you notice? A: It looks like there are a greater number of right handers performing more poorly than left handed batters and switch hitters. The tables below help to show the relationship between handedness and batting avg/ home runs.
4. Q: What do you think is the main takeaway from this visualization? A:Left handed players may have an advantage that helps them not perform as poorly as right handed players. But the better right handed players are able to get as many home runs and as high a batting average as their counterparts.
5. Q: Is there something you don’t understand in the graphic? A:It would be nice to see how many pitcher positions are in each group of handedness. 
6. Q: Do you have a recommendation? A: It would be great to be able to take away data from the scatter plot to reveal more of the points, or remove some of the “possible outliers” the increase the resolution of the X axis.


#### Feedback 2:

1. Q: What do you notice in the visualization? A: Both visualizations do a good job of displaying data. I do see that the colors representing handedness do change from graph. The scatter plot shows the relationship between handedness and player’s ability well. Though the findings may not be too discernable from this first quick pass. 
2. Q: What questions do you have about the data? A: Are there better measurements or data for looking at ability than average and HRs? I know a common baseball stat is power, which might be good to use. Also what amount of pitchers are in this data set, because the American league and National league utilize pitchers differently in offense.
3. Q: What relationships do you notice? A: There seems to be a positive relationship between Homers and batting average.
4. Q: What do you think is the main takeaway from this visualization? A: Lefties look like they perform better vs. right handers. When looking at Homers and batting average and not taking anything else into account. This seems to be what most people think in baseball too, or at least what I have heard.
5. Q: Is there something you don’t understand in the graphic? A: No there isn’t, pretty straightforward.
6. Q: Do you have a recommendation? A: Going back to the first question, the colors are different for each handedness between the 2 graphics, maybe change those to match up. Example: switchitter is yellow in the bar chart and scatterplot. Also there are some spelling and grammatical issues you might want to clean up.


#### Feedback 3:

1. Q: What do you notice in the visualization? A:The bar chart tells us about the number of players by group, the group being handedness. The scatterplot aims to draw comparisons between the handedness groups concerning the variables of homeruns and batting average.
2. Q: What questions do you have about the data? A: I was curious about some of the summary stats of the data, some of these were addressed in the text.
3. Q: What relationships do you notice? A: There is the relationship between handedness percentage of the group, as well as the scatterplot’s bivariate relationship between homeruns and batting average.
4. Q: What do you think is the main takeaway from this visualization? A: Left handed players in the MLB perform slightly better than right handed players, the same may also be true for switch hitters.
5. Q: Is there something you don’t understand in the graphic? A: The color difference between the two graphs threw me off for just a sec, other than that nope.
6. Q: Do you have a recommendation? A: You should fix the colors to match between both graphs, and also see if you can clean up the scatter plot a bit, there is a ton of info all lumped together. Maybe either make it so only some data can be viewed at a time, or that there is an opacity for the circles. Perhaps you might want to include some more stats about the averages or medians. Other than that looks good!

### Resources
Resources - list any sources you consulted to create your visualization

References are listed below: 

1. Holder, M. K. (1997). "Why are more people right-handed?". Sciam.com. Scientific American Inc. Retrieved 2008-04-14.
2. Annett, Marian (2002). Handedness and Brain Asymmetry. Psychology Press.
3. http://www.newsweek.com/science-why-lefties-make-better-baseball-players-92783
4. http://blogs.discovermagazine.com/discoblog/2008/07/08/why-do-so-many-lefties-play-baseball-its-built-for-them/
5. http://dimplejs.org/advanced_examples_viewer.html?id=advanced_interactive_legends
6. https://stackoverflow.com/questions/21045368/change-bar-color-in-a-vertical-grouped-bar-with-dimple



