# Version 0.4.0 - Change Notes
This version aims to address several key issues identified in version 0.3:
- In 0.3, even with several improvement types added, the board still felt somewhat irrelevant and divorced from development cards, which were the game's strongest mechanic.
- The war mechanics, while mostly functional, were not particularly fun.
- The complexity of food tracking was very high without much payoff.
- The technologies, while interesting, presented a lot of information and sometimes felt irrelevant.

To address these issues, we've made several significant changes:
- Replace the "round" structure with simple rotating turns.
    - Instead of drafting a finite set of development cards each round, the player who's turn it is simply chooses from five face-up development cards, and then draws a one from the deck to replace it. 
    - Battles now trigger immediately when a player moves a regiment into an occupied province.
- Remove food as a resource, and replace it with a status: your empire is either "fed" or "well-fed", and if it isn't well-fed, it can't urbanize.
- Add roads as a new improvement, to increase the board's strategic depth. Roads are used to connect provinces, which matters for food, urbanization, movement, and Commercial Booms.
- Replace the Global Event system with Population Booms and Commercial Booms --- events that fire in specific provinces, with some warning, so that players have an incentive to try to gain control of or connection to those provinces.
- Reduce the number of technologies from 5 types with 4 levels each to 3 types with 3 levels each.

# 1800 - Rules & Strategy Guide

## Overview
1800 is a historical strategy game set in 19th Century Europe. The game can be played by 2-8 players, each leading of one of eight European powers: Great Britain, France, Prussia, Austria, Russia, Spain, Italian States, or Ottomans. For 120 years (starting in 1800, divided into three eras), players compete for economic and military dominance. In 1920, the player who's built the most prosperous empire -- and done the best job fulfilling their empire's secret "national ambition", will be crowned the victor.

## Game Contents
1. Board: a map of Europe, divided into countryside and urban provinces.
2. Starting Mats: one for each player, showing with default policies and technologies, with a place to track your prosperity.
3. Player Tokens: colored discs (citizens); colored cones (regiments); colored rings (trade tokens).
4. Resource Tokens: blue cubes (production); green cubes (commerce)
5. Other Tokens: black rectangles (factories); large gray discs (urban centers); brown narrow rectangles (roads); pink cube (for prosperity-tracker).
6. Cards: admin cards; military cards; national ambition cards; province cards; development cards (which includes policies, institutions, and technologies).

## Gameplay Concepts

### Prosperity
The goal of the game is to have the most prosperity at the end of the game. There are several different ways to increase your prosperity throughout the game, but there are also opportunities to *spend* the prosperity you've gathered to further your military or industrial aims. While this may same like moving away from your goal, it can jump-start your growth and give you a chance to regain that prosperity, and then some, before the game ends.

### Citizens
Your empire is nothing without its people --- represented in this game by small colored discs and referred to as "citizens". Each citizen resides in a single province, and may or may not be placed on an improvement in that province. A citizen that is not on an improvement is referred to as a "peasent". A citizen on a farm is "farmer"; on a factory is a "laborer"; on an urban center is a "bourgeois".

### Regiments
Regiments are special units that you place on the board when you play a Standing Army card. Regiments can be used to occupy provinces, and can help you take permanent control of provinces by oppressing or massacring foreign citizens. A province can only have one regiment in it at time: 
- It is always illegal to move a regiment into a province where you already have a regiment. 
- You may move a citizen into a regiment with a regiment belonging to another player, but when you do, a battle will occur, and the losing regiment will be expelled.

### Province Control
Many crucial mechanics depend on who controls a province. For instance:
- You can only migrate citizens into provinces you control.
- When there is a Population Boom in the province, new citizens will belong to the player who controls the province
- You must control a province to benefit from commercial booms in connected cities.

Control of a province is determined as follows:
- If there is a regiment in the province, the province is controlled by the regiment's owner.
- If one player has more citizens in a province than every other player, than that player controls the province.

It is possible for a province to not be controlled by any player. 

Citizens in a province that is controlled by a player are referred to as "occupied citizens" (if there is a regiment in the province) or "minority citizens" (if there is no regiment in the province). Occupied and minority citizens still produce resources for you, but beware -- they may be vulnerable to oppression, conversion, or extermination.

### Improvements
Improvements are features that can be built in provinces, or, in the case of roads, between provinces. Once an improvement is placed, it remains there for the rest of the game, unless it is explicitly destroyed by a player action. Cities can support 5 improvements, while countrysides can support two. If a province is at it's maximum number of supported improvements, a player who wishes to build a new improvement on that province may destroy an existing improvement. 

There are five types of improvements:
- **Factories** provide +1 production per turn when worked by a citizen. Factories may only be placed in urban provinces. Initial cost: PPP.
- **Farms** support one laborer or bourgeois when worked by a citizen. Farms may only be placed in countryside provinces. Initial cost: PP.
- **Roads** connect provinces, allowing farms to support connected provinces and spreading the benefits of commercial booms. Roads can be built between any two provinces that share a land border. Initial cost: P.
    - Once you acquire the "Railroad" technology, you may place two roads on a single border between two adjacent provinces. These double roads are referred to as **Railroads**.
- **Urban Centers** are unique improvements that exist in each urban province at the start of the game, but cannot be built. An urban center with 2-4 citizens is considered a "City", and provides +1 commerce when a commercial boom occurs in a connected urban province. An urban center with 5+ citizens is considered a "Metropolis", and provides +2 commerce when a commercial boom occurs in a connected urban province.

### Feeding Your Laborers and Bourgeois
Peasants and farmers do not need to be fed: peasants are essentially subsistance farmers, and farmers can be supported by their own farms. Laborers and bourgeois, however, need to be supported by worked farms. One worked farm feeds one (and only one) connected laborer/bourgeois. In addition, a foreign trade route can feed one worker for each food icon on the trade route.

At all times, your empire is either considered "well-fed" or "under-fed". If all laborers and bourgeois are fed by a connected farm, your empire is well-fed. Otherwise, it is under-fed.

### Connected Provinces
To support urban citizens and spread the benefits of Commercial Booms, you'll need to connect your provinces using roads. Two provinces are considered connected for a given player if they are connected by a contiguous path of roads and/or sea crossings (represented by dashed lines), with the following restrictions:
- A connection cannot pass to or through a province that is occupied by a regiment of a country that you do not have a Free Trade agreement with.
- A connection cannot pass over a sea crossing if a player who you do not have a Free Trade agreement with has a larger navy than you.

Note that "connected" and "adjacent" provinces are different concepts. Two provinces can be connected but not adjacent if they are connected via multiple roads or sea crossings, and two provinces can be adjacent but not connected if they are next to each other but do not have a road between them -- or if one of them is occupied by a hostile regiment. 

### Cards
There are five kinds of cards in 1800, each with it's own unique card-back: Admin Cards, Military Cards, Development Cards, Province Cards, and National Ambitions.

#### National Ambitions
National Ambitions are drawn randomly at the beginning of the game. Each gives the player and secret way to earn victory points.

#### Province Cards
The Province Deck contains one card for each province. At the beginning of the game, turn 10 province cards face up, and place them where everyone can see them. At the start of each turn, the player whose turn it is will choose to trigger Population or Commercial Booms in two of the 10 provinces.
 - Population Booms occur in countryside provinces. If the province is controlled by a player, that player adds one citizen to that province. In Era II, they instead add two citizens. In Era III, they add three citizens.
 - Commercial Booms occur in urban provinces. Each player gets +1 commerce for each City they control connected to the province, and +2 commerce for each Metropolis they control connected to the province.

#### Admin & Military Cards
Admin and Military Cards are playable action cards that grant immediate effects when played. They're earned primarily by activating specific Development Cards, though you also get Military Cards for losing battles. Both Admin and Military Cards are secret, and can be held for as long as you want before you choose to play them. Military Cards can be played during battles to give bonuses to your armies, while Admin Cards can be played at any time during your turn. In addition, some Admin Cards specify other times when they can be played.

#### Development Cards
Development Cards are at the core of 1800: they define the shape and style of your empire, and over the course of the game it's Development Cards that will allow you to transform from a pre-industrial nation with minimal production capabilities to a flourishing empire with bustling commerce and mature political institutions.

Development Cards, unlike Admin & Military Cards, are not held in a "hand". When you pick a Development Card, you play it immediately, placing it face-up on the table in front of you. Once in play, some Development Cards grant effects, specified on the cards.

In many cases, resources can the placed on Development Cards, as indicated by squares depicting a hammer (production) or coins (commerce). On some cards, this will grant a static effect. When sufficient resources have been placed on the card, you may "activate" the card, which may involve an additional cost, like discarding an Admin Card. When you activate the card, remove all resources that you've placed on the card, and then gain the reward described on the card. For instance, if you've placed three production and an Industrial Policy card, you can activate it during your turn by discarding an Admin Card. When you do, remove the three production from the card, and build a factory.

Development Cards come in three varieties. All have the same card-back and are placed in the Development Deck together, but each has unique characteristics:
- **Policies** are cards that define the core political, economic, and industrial structure of your empire. You'll have three Policies active at all times: one political, one economic, and one industrial. When you play a new Policy, place it on top of your existing policy of the given type, replacing that policy. You start the game with three basic policies: Autocracy, Early Industrialization, and Landed Gentry
- **Technologies** are cards that define the level of technologic advancement your empire has achieved. You'll have three Technologies active at all times: one Agricultural Technology, one Military Technology, and one Infrastructure Technology. Just like with Policies, when you play a new Technology, it will replace an existing one. Technologies, however, are simpler than Policies: there is only one technology of each type to advance to in each era, representing the next "level" of that technology.
- **Institutions** are cards that define the various governmental and non-governmental features of your empire. While there are strict limits on how many Policies and Technologies you can have, there is no limit on your Institutions; you can even have multiple copies of the same card.

### Battles

A battle occurs when a player moves a regiment into a province that already has a regiment belonging to another player. The player whose turn it is is considered the "attacker"; all other players are with citizens a regiment in the province are consdiered "defenders". The battle proceeds as follows:
1. Play military cards. The attacker and defender take turns playing military cards, starting with the attacker. On their turn, a player may either pass or play a single military card. When a player passes, the other player can then play as many military cards as they choose, after which the battle ends.
1. Determine the winner. Players score battle points as follows:
1. The players receive battle points from their military technology.
    - The player with more citizens in the province gets one battle point. If the players have the same number of citizens in the province, neither gets a battle point.
    - The players get one battle point for each regiment in a province adjacent to the battle.
    - The players get battle points from any relevant military cards they played during this battle.
    - The player with the most battle points wins the battle. If both players have the same number of battle points, the defender wins.
1. Resolve the battle. The losing player must move their regiment out of the province, to an adjacent or connected province they control. The losing player draws a military card. Then, if the losing player has citizens in the province, they lose one prosperity.

## Gameplay

### Game Setup

#### Starting Citizens
At the start of the game, each player will have 8 citizens: 4 peasants in countrside provinces, 2 laborers on factories in urban provinces, and 4 farmers on farms in countryside provinces. All provinces that do not have a player citizen in them will have one neutral citizen.

There are a number of standard starting positions, depending on the number of players. If you do not use a standard start position, you may create your own starting position as follows:
1. Each player draws a random Province Card, and places a citizen in the drawn province.
2. Players take turns placing citizens in an empty province adjacent to a province they control, using a "snake draft" pick order.
3. Once each player has placed 8 citizens, place a neutral citizen in every empty province.

#### The Starting Mat
Each player gets a Starting Mat, which shows 6 starting development cards:

Starting policies
- Starting Government: Autocracy. C -> Draw an admin card.
- Starting Industry: Early Industrialization. PPP --discard_admin--> Build a factory. You may place no more than 1P on a single card on a single turn.
- Starting Economy: Landed Gentry: CCC -> Add one prosperity.

Starting technologies
- Agriculture: Cast Iron Plough. PP -> Build a farm. Max two farms per province.
- Infrastructure: Roads. P -> Build a road.
- Military: Muskets. +0 to all battles.

When you acquire new policy and technology cards, place them on top of the starting policy of the same type.

#### Decks and Cards
After setting up the board, you'll need to set up six decks: 
- The Admin Deck
- The Military Deck
- The Province Deck
    - Turn 10 Province Cards face-up to start the game.
- Three Development Decks, one for each era. When you all cards from the Era I Development Deck have been drawn, the second era starts, and you begin drawing from the Era II deck.
    - Turn 5 Development Cards from the Era I deck face-up to start the game.

#### National Ambition
Lastly, before starting the game, each player draws a random National Ambition card. Look at your National Ambition, but do not share it with others. At the end of the game, you will receive victory points that, along with your total prosperity, will determine who wins the game.

### Player Turns
The player who bears the closest physical resemblance to Napolean Bonaparte goes first. The game takes place in turns, starting with that player and proceedint to the left.

Each player's turn proceeds as follows:
1. **Population and Commercial Booms.** Choose two cards from among the 10 face-up province cards. Population/Commercial Booms occur in those two provinces.
    - If you choose a countryside province, you trigger a Population Boom. Add two peasants to the chosen province.
    - If you choose an urban province, you trigger a Commercial Boom. Each player gets +1 commerce for each City they control connected to the province, and +2 commerce for each Metropolis they control connected to the province.
        - A "City" is an urban center with 2-4 bourgeois.
        - A "Metropolis" is an urban center with 5 or or more bourgeois.
1. **Development card draw.** Choose one:
    - Choose a development card from the development card pool, then draw a card from the development deck to replace it.
    - Draw an admin card.
1. **Collect resources:**
    - Collect one production token for each of your laborers.
    - Collect production as specified by your overseas trade routes.
    - Collect commerce as specified by your Development Cards (economic policies and stock exchanges)
    - Collect one commerce for each of your trade monopolies. A  trade monopoly is any trade route that is not shared with any other players.
1. **Place resources on Development Cards.** Colored squares on the development cards indicate how many of each resource can be placed on the card.
1. **Activate Development Cards.** Development cards with arrows on them can be activated. Some cards have a cost to activation, like discarding an Admin Card. When you activate a card, you get the indicated reward immediately. Note that each Development card can be activated only once each turn.
1. **Regiment Actions.** Each of your regiments may make one action, which can be any of the following:
   - Move. Move the regiment to an adjacent province. If the province contains a regiment belonging to another player, a battle occurs.
   - Convoy. Move the regiment to a province connected via railroad.
   - Pillage. Remove an improvement from the regiment's province.
   - Oppress. Remove a foreign citizen from an improvement in the regiment's province.
   - Massacre. Remove a foreign citizen in the regiment's province from the board. Lose one prosperity. The removed citizen's controller may take an action with one of it's regiments.
1. **Citizen Migration.** You may move one peasant to an adjacent province. Then, you may move any number of peasants onto an unworked improvement in any connected province you control if, after the citizen has moved, your empire is well-fed.

### Ending the Game
When all development cards have been drawn, the game ends. Each player reveals their National Ambition and gains an associated bonus to their prosperity. The player the most prosperity wins.
