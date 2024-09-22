# StratHacks 
## What is this (background and information)?
In 2023, inspired by our experiences at Pennapps, we hosted our own hackathon, Trojan Hacks -and it didn't go nearly as well as we expected. As we found out, high school don't exactly have the resources nor the clearances to allow students to host overnight hackathons, and when your hackathon can only last about 6 hours, people find it really, really difficult to get work done. In fact, the number one feedback point for our hackathon was to make it more focused: the number one trouble that people had was simply finding an idea, even though we already gave them a prompt.

Later, talking to other high school hackathon organizers, we found out this was a fairly common problem (which is why high schools tend to host competitive coding competitions rather than hackathons). Whether it be Zayan Jami from Teen Hacks Long Island, or Rohan Phillip from the east coast, high school hackathon organizers have the same problem: how do we find a middle ground broad enough that allows our hackers to still be creative and free with their ideas, but also specific enough that they don't have to spend too long debating ideas? 

In discussing ways to solve this problem for our next hackathon: one idea came up. Reminiscent of how Robert Axelrod simulated the Prisoner's Dilemma all the way back in the 1980s, we could simply give our hackers a platform with a game they would compete in, equip that platform with a simple way for them to write a bot that plays that game, and then let them compete. Beyond being a fun hackathon theme and event, when published, this would also allow other to explore lengths of strategic coding, game theory, and competitive technique, all through the lens of a fun game to simulate. 

Thus, at this hackathon, StatHacks was born. Utilizing a Visual Studio Collaborative session and Flask for python, we build a webapp that anyone can read how to create a bot according to a game's specifications, build it, upload it, and run it against other bots they've created. From complex games to be used in hackathons, like Poker, to simple games to be used as a fun daily puzzle, like higher or lower, StatHacks allows users to finally put their strategic minds to work.

Unsurprisingly, it was difficult. Right off the bat, we were immediately disadvantaged by both internal conflicts, and the fact that our team only managed to gather a total 2 people. Only one of us had any experience with Flask, and aforementioned experience had taken place years ago. Yet, through a couple late nights, long hours of code, a lot of caffeine, a decent amount more of internal conflict, and a single poker game, our app was born. We utilized Flask in order set up a backend for our website; a custom API in order to catagorize player and game data for each game we designed; libraries to receive the user's files; many, many libraries in order to call functions from user's uploaded files; custom game logic, written from scratch, in order to run the games while updating aforementioned API properly; and finally, a whole lot of CSS custom design to make the website look pretty decent. At the end of it all, we had what we wanted to make and more: a webapp that looked nice, functioned properly, delivered a satisfactory user experience, and allowed those high school hackathon organizers to have a little bit of a better time. 

Whether it's complex enough or well built-enough for an award, we can't say. But we can say that we've tested it - and, in our very humble non-biased opinion, it's pretty darn fun. So, give it a try! And if you're a highschool hackathon organizer, maybe bookmark this post for later.




## BASIC RUNDOWN OF THE CODE:
CODE IS FORMATTED AS IS STANDARD FOR THE MAJORITY OF FLASK PROJECTS
##
Templates contains HTML/CSS files used for each webpage
##
uploads is the folder for user uploaded data onto the webpage
##
app.py stores the endpoint logic for flask as well as allk the eneded functions that accompany it.
##
pycache files can be ignored - they're basically for bookkeeping, the code generates them to run methods within each of the uploaded files. Pay it no mind if you're not interested in that kind of stuff
##
overall the code is pretty simple and intuitive, just make sure you have it all because it does rely on each other. 
