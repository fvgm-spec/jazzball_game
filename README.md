# JazzBall Game

A simple interactive game inspired by JazzBall, built with Pygame and Python.

## Game Description

JazzBall is a casual arcade game where you control a green ball with your mouse. The objective is to collect yellow target balls while avoiding red obstacle balls. Each level increases in difficulty by adding more target and obstacle balls.

## Features

- Interactive gameplay using mouse controls
- Demo mode to watch AI play the game
- Multiple levels with increasing difficulty
- Score tracking
- Simple collision physics
- Clean menu interface
- Screenshot functionality

## Controls

- **Mouse Movement**: Control your player ball
- **ESC**: Return to menu
- **R**: Restart the game
- **F12**: Take a screenshot
- In menu:
  - Click "Play Game" or press 1: Start playing
  - Click "Watch Demo" or press 2: Watch AI demo

## Requirements

- Python 3.x
- Pygame

## Installation

1. Make sure you have Python installed
2. Install Pygam
e: `pip install pygame`
3. Run the game: `python jazzball.py`

## Game Mechanics

- **Green Ball**: Player character
- **Yellow Balls**: Target balls to collect (10 points each)
- **Red Balls**: Obstacle balls to avoid
- Complete a level by collecting all yellow balls
- Game over if you hit a red ball

## Demo Mode

The game includes a demo mode where an AI plays the game. The AI will:
- Target the closest yellow ball
- Try to avoid red obstacle balls
- Automatically progress through levels

The demo will run for 30 seconds before returning to the menu.

## Project Documentation

Check out the blog post in `blog_post.md` for a detailed discussion about:
- The development process
- AI-assisted game development techniques
- Code examples and explanations
- Screenshots and gameplay details
