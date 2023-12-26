# AdventofCode2023
Solutions for the [Advent of Code 2023](https://adventofcode.com/2023) coding puzzles!

## Strap yourselves in for a breakneck speed run-through of my favourite days and what I learned from them!

### Day 1: Trebuchet?!
Part 1 had us finding the first and last digits in strings. Easy enough right? For example '1abc2' would return 1,2 and 'treb7uchet' would be 7, 7. Hahahah if only it were that simple.
Part 2 took this to a whole new level and is by far the hardest Day 1 puzzle I have seen. Now the digits can be spelled out too! So 'two12nine' would not be 1,2 but actually 2,9! 
I constructed a graph of all the starting characters in the digits 0-9 and treated this as a predictive text problem. For example, Looking at the input one at a time, if I see an 'f' then I have edges to 'I' (five) and 'o' (four) as possible next characters. If we don't see either of them we scrap it and start again! 'oneight' became my living hell all day and taught me the importance of proper test cases right away which I took forward to every day to follow. Is this the easiest solution, aaabsolutely not, but it was really fun and I tried something new

### Day 5: If You Give A Seed A Fertilizer
This Day is infamous now and may just be the hardest and most rewarding day on the whole list.
We start with a seed, say 79. Every seed needs a type of soil to be planted in, simple enough for example: seed -> soil map could look like 79 -> 81. However, soil needs a special fertiliser, fertiliser needs a special water, water needs a special light, light needs a special temperature, temperature needs a special humidity and to round us out,  humidity needs a special location in the garden! For example seed 79 -> 81 -> 81 -> 74 -> 78 -> 78 -> location 82.
For Part 1 this is very manageable, we have 20 seeds and need to find the one with the smallest location. 
For Part 2 however, we end up needing to check an intractable something like 14 BILLION SEEDS!
Many solutions I saw online afterwards used some parallel processing, a compiled language, and a few hours to crack it, but I really wanted to figure this out properly as there must be a better way, right?
Well let's take a look at how the maps work. '53 50 10' for example could mean that starting at seed 50 that gets mapped to soil 53, we go to seed 59 that gets mapped to soil 62.
You'll notice that if im checking any seed between 50 and 97, the same thing happens. This means that instead of checking every seed in the range (which in the full problem are millions/billions of seeds long) we just need to see what happens to the start and end points!
I thought this might be possible but wasn't sure at all. As this competition is just for the fun of learning for me, I looked to see what other people had been doing on Reddit and 'range splitting' was being discussed. As soon as I knew my idea was along the right lines I went for it, and it worked! 
The basic idea is like this:
I start with my range of all possible seeds e.g. (1,100)
If I come across a rule, e.g. 53 50 10 from before, then seeds (1, 49) are unchanged so this is one split range, the seeds (50, 59) is another split range that now becomes (53, 62), and finally the original seed range (60, 100) is also a third split that remains unchanged.
I ended up needing 6/7 different cased for possible ways these ranges can overlap as you can see in the day5p2.py code. I am very glad I did this though as it takes execution time from years to a split second!

### Day 6: Wait For It
A quick shoutout to Day 6 for being a really nice rest after Day 5, easily the easiest day of the year and funnily enough completely solvable with just a pen and paper, much more like Advent of Math, but a fun problem none the less! I mention it because this day primed for the fact that not every day is purely coding something up, but that more heavily mathametical research might need to be done... and oh boy will I come back to this later

### Day 7: Camel Cards
I absolutely loved today as I am a sucker for recreating games, and today was all about a version of Poker with rules that are easier to play on a Camel, because obviously that's a problem we all face every day!
I also remade Luigi Poker from the New Super Mario. Bros DS Minigames a few years ago so I feel READY!

There are 7 different types of hand you can have:
1. Five of a Kind
2. Four of a Kind
3. Full House
4. Three of a Kind
5. Two Pair
6. One Pair
7. Junk
   
Today is a favourite because of all the ways to determine which type of hand you have, I think the way I did it is really quite nice.
For example lets have the hand 'A23A4'. This is obviously just a single pair to us, but here's how I wrote the classifier algorithm:
First we want to get how many times each of the type of cards appears in the hand. That gives us a dictionary where the key is the type and the value is the count: {A: 2, 2: 1, 3: 1, 4: 1}.

The second step is to realise we don't really care about just how many of each type we have, but how many times we have the same number of a type. In this example we have 2 of a type once (the 'A') and we have 1 of a type four times (the '2', '3', and '4'). this gives us a new dictionary following the same process again: {1: 3, 2: 1}

It is now this matching counts dictionary that we can use to determine the hand. You can see the full logic in the 'get_type_from_matching_counts' function on line 13 of day7.py, but to finish of this example, 5 isnt a key in this dictionary, so we cant have a 5 of a kind. The same story for 4 not in for 4 of a kind, and 3 not in for Full house and 3 of a kind. That leaves 2 pair, 1 pair or junk. We can rule out junk because a junk dictionary would by definition have to be {1: 5}. As we know we now only have either a 1 Pair or a 2 Pair, we can see that a 1 Pair dictionary would be {1: 3, 2: 1} and a 2 Pair dictionary would be {1: 1, 2: 2} as the only options. Luckily for us that would tell us this hand is a One Pair, which is correct.

### Day 8: Haunted Wasteland
Day 8 was very tricky. You'll see a lot of discussion added to the Day 8 folder which is unique to this day. That's because the solution was based on a few assumptions that definitely do not work in general, meaning the input was carefully crafted to make sure the method of using LCM or Lowest Common Multiple of different paths did in fact work to find the number of steps until everything lines up.
Personally I tried LCM because I coudn't think of anything else to do, and was delighted to see it work. I have to thank my Elementary Number Theory module last year for this one otherwise I wouldn't have had the background to immeditely recognise it as a possibility (Advent of Math making a comeback). This also dictated a turning point for AOC in my mind. I though every day was more of a programming problem with a general solution, but today was very much more of a puzzle; play around with the specific inputs I have been given and spot/explore to find patterns that make it easier to solve. I didn't like this at all on the day, but reflecting on it now I am really glad I accepted this early in the month and came to enjoy it, because there are some days later on that this is absolutely required to treat them as puzzles, and I really, really enjoyed them. 

### Day 9: Mirage Maintenance
Todays puzzle was Advent of Math again, but I was so excited when I thought of my approach I coudn't stop thinking about it all day! 
We are given a list of numbers e.g. '0 3 6 9 12 15' and we have to extrapolate to find the next next element in the sequence! The problem description expalined how to do this by finding the differences of rows until you reach 0:
```
0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0
```
But as soon as I saw this pattern I stopped reading and had a brainwave! Thank you GCSE/A-Level Maths because this is exactly how we found the formula for the nth term then, by writing a little line with the differences underneath and plugging them into a formula. Back then we only dealth with simple quadratic sequences, but Thank you University Computer Science and Maths Degree because last year I studied Lagrange Polynomials. 'In numerical analysis, the Lagrange interpolating polynomial is the unique polynomial of lowest degree that interpolates a given set of data'. Implementing this led me to use sympy for the first time, and I learnt so much! (This knowledge also helped me solve the otherwise impossible day 24!) Was finding the formula for the nth term completely over the top when they only wanted to next term? Absolutely. Was it worth it because it was really fun and rewarding? Even more so!

### Day 10: Pipe Maze
The interesting part of today was working out how to tell if a point is inside or outside of a polygon. Luckily for me I know an algorithm for this as it's quite common to need in game development. The 'Point in Polygon' algorithm I was familiar with is to cast a ray from the point outwards in any directions and count the number of times you cross the polygon. If its even you are inside the shape and if its odd you are outside the shape. In research for this question I also came across the Winding number algorithm and an [amazing visualisation](https://twitter.com/FreyaHolmer/status/1232826293902888960) of it by the wonderful Freya the 'shader sorceress' and reason I know how to code pretty much anything to do with graphics and polygons. 
The challenge of today came from discretising the algorothm to work not for a defined polygon in 2D space, but for just a set of points on a grid, but I got there in the end!

### Day 12: Hot Springs
Hot Springs is a very apted name for the day that put me in very hot water. I struggled with this one for hours and knew that dynamic programming was the way to go, but it was figuring out the best implementation of it that determined whether the algorithn would run in a blink or days. Unashamedly I did end up looking for [help](https://advent-of-code.xavd.id/writeups/2023/day/12/) on this one. I am happy to say though that my idea for solving it was 100% correct, I was just overcomplicating the implemtation itself. Today I learnt about functools 'cache' to make it a easy as one '@cache' above the function definition, and all my problems went away!

### Day 13: Point of Incidence
The first and only day I did a little code golfing! I really enjoyed how simple this one because when I realised it was best thought of as an error correction problem, with hamming distance describing how corrupted the mirror is. This was my first time implementing it, and was fun! This was also my first time using the 'next' keyword in python. I found quite a few syntactic sugery things out about python this year, some really cool and other probably best avoided... For a little fun though I think this was pretty nice. (And much better than a discovery I made a little later on...)

### Day 14: Parabolic Reflector Dish
Today was another little game implementation, woo!
We start with a grid of sliding rocks and walls in the way
```
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
```

And can tilt the grid so that the rocks all slide in a certain direction, for example after a tilt north this grid will look like:
```
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
```

Part 1 was really nice, we simply tilt for '1 cycle' where a cycle is tilting north, then west, then south, and then east. There was a potential hang up with moving the rocks as in the following scenario:
```
O
O
.
O
.
O
```

If we are tilting north and moved the bottom rock first, it would hit the rock above it, stop, but then that rock itself would move out of the way and look something like this, which is definitely wrong:
```
O
O
O
.
O
.
```

Luckily for me, I already solved this problem before [when I recreated BABA IS YOU](https://www.youtube.com/watch?v=-YQjwvbePnE), and even made a visualiasation for it in the devlog which I would recommend if you want to see it explained in more detail.

Part 2 today though was initially ROUGH. I mentioned part 1 had us run 1 cycle? well for Part 2 we had to run 1000000000 cycles!
This is obviously not possible, but we have to do it anyway! 
After some thinking I had the thought that if I was to perform 1000000000 cycles on this example grid above, there aren't even anywhere CLOSE to 1000000000 possible positions the rocks can be in, so by the pigeon-hole principle, the positions the rocks are in after each cycle MUST repeat at some point. I called the number of cycles this takes the rocks period. For example if we are doing 112 cycles, but the rocks positions completely reset to the original after 10, then after 110 cycles we are back at the original position - and we only really need to run it for 2 cycles to get the answer!

### Day 15: Lens Library
Well today wins the award for easier Part 1, by FAR!
Part 2 was also very easy but only because I recognised what was going on, it was perfectly creating our own hashmap from scratch! Not something I had done before but I really enjoyed it, and was also the first time I wrote some classes 'Node' and 'LinkedList' to help out

### Day 16: The Floor Will Be Lava
Nothing special about today other than me making the BEST DISCOVERY IN PYTHON EVER... the [Walrus operator](https://towardsdatascience.com/the-walrus-operator-in-python-a315e4f84583). It's silly and bad practise, but it's SO FUN!

### Day 18: Lavaduct Lagoon
It was around Day 18 that things really started to get involved. Needing to research theorems I may have not seen before or getting out some pen and paper to really explore the problem more. Luckily for me though this is the part I was really looking forward to as it's the best chance for learning! 
So many problems now have involved some kind of 2D grid I took time to write my own package so I can reuse the code between days, and for any future projects too. This turned out a really good idea. I learned about making frozen dataclasses, 
adding the ability to use '+', '*' etc for custom classes, and most importantly for this problem, defining my own polygons with vector2 points. 

The problem resolved to having a set of points on a grid that acted as a perimeter, and needing to work out the area of the shape. My first idea was to use a floodfill algorithm and quite literally just find every single grid point inside the shape that way. While this worked for smaller grids, the problems input was far too large for this to work quickly. 

I went in search of other theorems for areas from set of points in a polygon, and came across the [Shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula) for area, and combined this with my own perimeter algorithm and discretisation to handle the thickness of the polygon as we are on a discrete 2d grid when this algorithm is meant for the full XY plane.

### Day 19: Aplenty
For Part 1 we have been given a set of points in 4D space, and need to apply some conditions to them to see if they pass or fail. for example, a part (100, 300, 4000, 2) would pass the test x > 200, but fail the test z < 2000. We simply check the set of conditions against the 541 given 4D points, no big deal and it runs as quickly as you could want. 
For Part 2, we have to check not just 541 points, but EVERY point in the 4000x4000x4000x4000 space. This is, a lot of points. We are in luck though, because have a completely intractable number of points to check and conditions that split them based on '>' and '<' ranges sounds awfully familier... It turns out Day 5 was an EXCELLENT training day for this one, and I knew right away range splitting was the way to go, and solved it in minutes instead of hours like it did the first time! I loved the AOC reused concepts from earlier and easier problems on the later days to really solidify knowledge and it really worked!

### Day 20: Pulse Propagation
Here we are. The most conceptually amazing day of the year that completely blew my mind. We have a network of 'Flip-Flops' that take a high or low pulse and send out the opposite, and 'Conjunctions' that take in multiple pulses and fire a high pulse if they are all the same and a low pulse otherwise... Sound familiar?

This is a NOT and AND Gate! When we put them together we can make a NAND gate, and NAND gates are turing complete, mmeaning todays puzzle has us building what is functionally a fully working computer, awesome!

What's not so awesome was Part 2, when it asked us to, quite literally, see after how many steps the program would terminate. There is a name for that problem, the Halting Problem, one of if not THE most famous and fundamental example of something that cannot be solved. Even just typing this now makes me excited because it's so amazing to me at how well crafted this puzzle was to make it possible. Not only was this possible for this very specific input, but it also combined other concepts from previous questions too! (I am slightly exaggerating because its not exactly stricly speaking the halting problem but it is close enough to make this the best puzzle I have ever seen)

The answer ended up being 243221023462303 steps. This is obviously far to large for me to have just let run and see when it terminates. I remembered Day 8 was also a problem turned puzzle that in general is much much harder to solve, and given how this one was impossible I knew that some puzzling must be going on here. 

The program terminated when module 'rx' fired. After some explorarion of the modules, 'rx' is a conjunction module with the modules 'ln', 'dr', 'zx' and 'vn' as inputs. I figured that although I cant wait for the full termination, I can instead terminate when each one of these previous modules are on, and go from there. 
This gave me 4003, 3863, 3989, 3943 as the number of cycles needed to have the previous modules turn on. With this, I made an assumption that they repeat at this period too. I checked upto 100,000 iterations and each one of them always only turned on at a multiple of 4003, 3863, 3989, and 3943 respectively so I was prepared to make that assumption. That would mean that, just like Day 8 again, using the LCM of these numbers would tell us when all of them are on at the same time, or 243221023462303.
I later found out some people went a step further and fully worked out that each of the 4 previous modules are binary counters that count up from 0 to their period and then go back to 0, which explains why it repeats perfectly!

### Day 21: Step Counter
This day is the only day I haven't completed fully. Part 1 was very doable, but Part 2 requires some knowledge that I couldn't figure out in time. I am very happy this problem exists as it shows me I have a clear and obvious place to learn from but for now I have to accept defeat. Watch this space, I'll be back to explain it fully when I get it in the new year!

### Day 22: Sand Slabs
...More effectionately called Exploding Tetris! Today was another game so I felt at home, and managed to solve it with a fairly uncomplicated algorithm. 
However, today is unfortunately around the day I really lost some steam in my solving as I was getting quite burned out from 22 days of continuous problems, especially after failing yesterday.

### Day 23: A Long Walk
Not much to say about today as it was a fairly simple one to understand. Write a LONGEST path algorithm and wait for it to finish. I think today's algorithm is the only one I have that doesn't solve the problem instantly and rather takes around 15 seconds. This was my first time ever looking for and implementing a longest path algorithm though as it doesnt particular come up much in real world applications I have been a part of. I found it really interesting to see that it's an NP-Hard (although unsurprising). This is because there is no way to decompose the problem with any kind of optimal substructure into one thats easier to solve or has any value in solving the larger one. From what I could tell the best method is brute-forcing it but with some clever optimisatons.

### Day 24: Never Tell Me The Odds
Back to Advent of Math! I really enjoyed part 1 as we had to look at different paths of hail stones moving with constant velocity, and seeing if they intersect with eachother anywhere. This was just some simple equation rearranging I explain in the code, with the only thing of note being to represent the paths with the most convinient format of start + velocity * time. 
Part 2 however is both the hardest and easiest thing I have seen this year and it conflicted me a little with my solution. We had to find a stone we could through that would hit EVERY other stone at some point in time along it's path. This initially seemed to me just like an outrageous simultaneous equation, and it was, but not in the way I expected. I knew this was what I had to do, but also know that I didn't want to write my own solver (perhaps another day). I had previously used sympy for the first time on Day 9 to make Lagrange Polynomials, so I used a imilar module Z3 (which I hadn't heard of before) to solve the system in a fraction of a second, and the least amount of code since I tried golfing. I am very glad to have discovered Z3 and how to use it, but it does feel a little like cheating to just throw this entire part into it in 6 lines with no other effort being needed.

### Day 25: Snowverload
We are given a graph in adjacency list form, and need to cut three edges to disconnect it into 2 connected components. This immediately screams to me maxflow-mincut, but as it was Christmas Day and I just yesterday set the prescedent of using external solvers, I used the christmas gift of the networkx module (which I also haven't used before so I was excited to try it) to find the edges needed to remove, actually remove the edges, and then find the connected components.
I would like to go back and solve this one manually (perhaps with Ford-Fulkerson) at some point without networkx, but I can take some pride that if I didn't notice it was mincut then I wouldn't have been able to use this module in the first place! Merry Christmas!
