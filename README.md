# Socially Intelligent Robotics: Trustability Study with Nao Robots

Group-1-main

Project Overview
This repository contains the research and code for the "Socially Intelligent Robotics" course project at [Vrije Universiteit]. Our project focuses on studying trustability in human-robot interactions by comparing submissive versus dominant behaviors in Nao robots.

## Objective
The primary objective of this research is to understand how different behavioral traits in robots, specifically submissive and dominant behaviors, impact the trustability perceived by human participants.

## Methodology
We use the Nao robot, a programmable humanoid robot developed by SoftBank Robotics, as the subject of our study. The robot's behaviors are programmed to exhibit either submissive or dominant traits in controlled interaction scenarios with human participants.

### Submissive Robot Behavior
* Exhibits behaviors like lower gaze, slower movements, and passive interaction patterns.
* Designed to appear more approachable and less threatening.
### Dominant Robot Behavior
* Demonstrates behaviors such as direct gaze, assertive speech, and proactive movements.
* Aims to assert authority and control in the interaction.

## Data Collection and Analysis
Participant Interaction: Each participant interacts with one of the submissive or dominant versions of the Nao robot while playing a trustability based game.
Data Points: We collect data on participant trust, name, place of birth among some other, and their willingness to openness to work with robots in their daily lives.
Analysis Tools: Data analysis is conducted using [a survey].


# Clone the repository
git clone git@github.com:SIR-2023/Group-1.git

# Navigate to the project directory
Make sure redis is installed and a connection is made to a NAO or NAOqi robot. 
* cd framework
* python nao_dominant_game_complete.py
* python nao_submissive_game_complete.py

# [Include any additional installation or setup instructions]
In order to run the experiment we created 2 separate scripts called nao_dominant_game_complete.py and nao_submisive_game_complete.py respectively. Together with the dialogflow service these are the 2 main scripts that we use.

## Contributors
[Group 1 ]
