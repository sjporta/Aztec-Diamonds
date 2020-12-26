# Aztec Diamonds

Pretty much what the title says. In response to this Mathologer video: https://youtu.be/Yy7Q8IWNfHM, I decided to tinker around with Pygame to make a program that randomly tiles an Aztec Diamond with 2x1 dominoes. At each step, it does the domino dance shown in the video, removing clashing dominoes and sliding the rest. The result is the so-called Arctic Circle Theorem, where the corners tend to be aligned in the same direction, and the center is a mess.  

This is still very much a work in progress, and I intend to implement some more polishing around the edges in the future.  

There's a preview below:  

https://user-images.githubusercontent.com/62448093/103145907-a1d76580-4717-11eb-923c-97b4d85b6b80.mp4  

Controls:  
ESC: Exit.  
Enter: Runs one full iteration (eliminates clashes, slides blocks, fills in empty 2x2s).  
R: Resets the board.  

