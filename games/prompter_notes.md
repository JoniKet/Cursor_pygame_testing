# Revenge of pigs

- First ever usage of Cursor IDE, familiar with the under the hood LLMS
- Cursor was able to generate game Assets completely on its own. Took the generated background, feeded it to gemini and asked for fancy enhanced background
- Really impressive features
    - I was able to take screnshot, paste that to the "Agent" mode, and it was able to improve UI based on the screenshot
    - When issue was faced, it added debugging log lines to the code and then was able to fix things based on those lines !


# Questioning Bird

- Generated 'game_creation_instructions.md' and started to use Claude 3.7 model to iterate on it. 
- Took quite a while for the agent to come up with anything relevant. This does not appear to be the best way to generate the simple game,
  should maybe give less instructions at the start
- Afterwards quite a bit of iteration, the Agent debugging on itself, the game got playable. Impressive.
- Asked the Agent to give the bird more thoughts, and make it also possible to "shoot" the player in case the bird got really angry
- Also asked the Agent to add sounds to the game. The Agent proceeded to install Scipy library to generate game sounds ?!
- Impressed by the sounds, asked the Agent to generate background music for the game. And it generated a script to do that as well ?!