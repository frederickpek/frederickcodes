# Klotski - Anything But A Kid's Puzzle

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Quo_Vadis-HABA.jpg/1024px-Quo_Vadis-HABA.jpg" alt="drawing" width="325" />
</p>
<p align='center'><sub>Figure 1: Klotski Puzzle.</p>

This sliding block puzzle may look very simple but trust me, it is exceptionally difficult! So much so that it drove me to employ my cpu to search for the solution with the least number of legal moves in a depth-first-search manner.

Klotski dates back to the early 20th century with many variations. The aim of the game is to remove the red block by sliding the blocks around the available space. The minimum number of moves for the original puzzle is 81, if you consider sliding a single piece to any reachable position to be a single move.

You can try the game of [Klotski](https://www.schoolarchimedes.com/klotski) for yourself!

### Sample Program Output (KlotskySolver.py)
Please pardon the lack of visuals for this project, i found it too tedious to implement the movements for the blocks, especially when L-shape sliding moves were part of the solution.

**Depth**: The number of legal moves into the solution

**Batch Size**: The number of possible board states found from board-state D-1, excluding previously explored board states

**Total States**: The total number of unique board states found since D=0
```
Depth: 0, Batch Size: 1, Total States: 0
Depth: 1, Batch Size: 8, Total States: 8
Depth: 2, Batch Size: 11, Total States: 19
Depth: 3, Batch Size: 15, Total States: 34
Depth: 4, Batch Size: 18, Total States: 52
Depth: 5, Batch Size: 18, Total States: 70
Depth: 6, Batch Size: 23, Total States: 93
Depth: 7, Batch Size: 28, Total States: 121
Depth: 8, Batch Size: 42, Total States: 163
Depth: 9, Batch Size: 42, Total States: 205
Depth: 10, Batch Size: 50, Total States: 255
Depth: 11, Batch Size: 44, Total States: 299
Depth: 12, Batch Size: 50, Total States: 349
Depth: 13, Batch Size: 46, Total States: 395
Depth: 14, Batch Size: 52, Total States: 447
Depth: 15, Batch Size: 43, Total States: 490
Depth: 16, Batch Size: 59, Total States: 549
Depth: 17, Batch Size: 62, Total States: 611
Depth: 18, Batch Size: 70, Total States: 681
Depth: 19, Batch Size: 64, Total States: 745
Depth: 20, Batch Size: 74, Total States: 819
Depth: 21, Batch Size: 48, Total States: 867
Depth: 22, Batch Size: 64, Total States: 931
Depth: 23, Batch Size: 81, Total States: 1012
Depth: 24, Batch Size: 91, Total States: 1103
Depth: 25, Batch Size: 113, Total States: 1216
Depth: 26, Batch Size: 156, Total States: 1372
Depth: 27, Batch Size: 197, Total States: 1569
Depth: 28, Batch Size: 187, Total States: 1756
Depth: 29, Batch Size: 240, Total States: 1996
Depth: 30, Batch Size: 295, Total States: 2291
Depth: 31, Batch Size: 373, Total States: 2664
Depth: 32, Batch Size: 456, Total States: 3120
Depth: 33, Batch Size: 487, Total States: 3607
Depth: 34, Batch Size: 551, Total States: 4158
Depth: 35, Batch Size: 650, Total States: 4808
Depth: 36, Batch Size: 717, Total States: 5525
Depth: 37, Batch Size: 774, Total States: 6299
Depth: 38, Batch Size: 906, Total States: 7205
Depth: 39, Batch Size: 946, Total States: 8151
Depth: 40, Batch Size: 1038, Total States: 9189
Depth: 41, Batch Size: 1084, Total States: 10273
Depth: 42, Batch Size: 1042, Total States: 11315
Depth: 43, Batch Size: 890, Total States: 12205
Depth: 44, Batch Size: 804, Total States: 13009
Depth: 45, Batch Size: 739, Total States: 13748
Depth: 46, Batch Size: 667, Total States: 14415
Depth: 47, Batch Size: 595, Total States: 15010
Depth: 48, Batch Size: 517, Total States: 15527
Depth: 49, Batch Size: 420, Total States: 15947
Depth: 50, Batch Size: 340, Total States: 16287
Depth: 51, Batch Size: 258, Total States: 16545
Depth: 52, Batch Size: 178, Total States: 16723
Depth: 53, Batch Size: 153, Total States: 16876
Depth: 54, Batch Size: 151, Total States: 17027
Depth: 55, Batch Size: 170, Total States: 17197
Depth: 56, Batch Size: 174, Total States: 17371
Depth: 57, Batch Size: 162, Total States: 17533
Depth: 58, Batch Size: 140, Total States: 17673
Depth: 59, Batch Size: 164, Total States: 17837
Depth: 60, Batch Size: 160, Total States: 17997
Depth: 61, Batch Size: 172, Total States: 18169
Depth: 62, Batch Size: 196, Total States: 18365
Depth: 63, Batch Size: 240, Total States: 18605
Depth: 64, Batch Size: 278, Total States: 18883
Depth: 65, Batch Size: 274, Total States: 19157
Depth: 66, Batch Size: 298, Total States: 19455
Depth: 67, Batch Size: 329, Total States: 19784
Depth: 68, Batch Size: 348, Total States: 20132
Depth: 69, Batch Size: 381, Total States: 20513
Depth: 70, Batch Size: 408, Total States: 20921
Depth: 71, Batch Size: 383, Total States: 21304
Depth: 72, Batch Size: 412, Total States: 21716
Depth: 73, Batch Size: 371, Total States: 22087
Depth: 74, Batch Size: 305, Total States: 22392
Depth: 75, Batch Size: 277, Total States: 22669
Depth: 76, Batch Size: 261, Total States: 22930
Depth: 77, Batch Size: 260, Total States: 23190
Depth: 78, Batch Size: 242, Total States: 23432
Depth: 79, Batch Size: 201, Total States: 23633
Depth: 80, Batch Size: 159, Total States: 23792
Solution found!
Minimum number of moves required: 81
Tracing the path used to reach solution.

Move sequence:

Move: 0
[ @   R   R   * ]
[ @   R   R   * ]
[ #   P   P   $ ]
[ #   o   o   $ ]
[ o           o ]


Move: 1
[ @   R   R   * ]
[ @   R   R   * ]
[ #   P   P   $ ]
[ #   o       $ ]
[ o       o   o ]


Move: 2
[ @   R   R   * ]
[ @   R   R   * ]
[ #   P   P   $ ]
[ #   o       $ ]
[     o   o   o ]


Move: 3
[ @   R   R   * ]
[ @   R   R   * ]
[     P   P   $ ]
[ #   o       $ ]
[ #   o   o   o ]


Move: 4
[ @   R   R   * ]
[ @   R   R   * ]
[ P   P       $ ]
[ #   o       $ ]
[ #   o   o   o ]


Move: 5
[ @   R   R   * ]
[ @   R   R   * ]
[ P   P   $     ]
[ #   o   $     ]
[ #   o   o   o ]


Move: 6
[ @   R   R   * ]
[ @   R   R   * ]
[ P   P   $     ]
[ #   o   $   o ]
[ #   o   o     ]


Move: 7
[ @   R   R   * ]
[ @   R   R   * ]
[ P   P   $     ]
[ #   o   $   o ]
[ #   o       o ]


Move: 8
[ @   R   R   * ]
[ @   R   R   * ]
[ P   P         ]
[ #   o   $   o ]
[ #   o   $   o ]


Move: 9
[ @   R   R   * ]
[ @   R   R   * ]
[         P   P ]
[ #   o   $   o ]
[ #   o   $   o ]


Move: 10
[ @   R   R   * ]
[ @   R   R   * ]
[ o       P   P ]
[ #       $   o ]
[ #   o   $   o ]


Move: 11
[ @   R   R   * ]
[ @   R   R   * ]
[ o   o   P   P ]
[ #       $   o ]
[ #       $   o ]


Move: 12
[ @   R   R   * ]
[ @   R   R   * ]
[ o   o   P   P ]
[ #   $       o ]
[ #   $       o ]


Move: 13
[ @   R   R   * ]
[ @   R   R   * ]
[ o   o   P   P ]
[ #   $         ]
[ #   $   o   o ]


Move: 14
[ @   R   R   * ]
[ @   R   R   * ]
[ o   o         ]
[ #   $   P   P ]
[ #   $   o   o ]


Move: 15
[ @   R   R   * ]
[ @   R   R   * ]
[ o           o ]
[ #   $   P   P ]
[ #   $   o   o ]


Move: 16
[ @   R   R   * ]
[ @   R   R   * ]
[         o   o ]
[ #   $   P   P ]
[ #   $   o   o ]


Move: 17
[ @   R   R   * ]
[ @   R   R   * ]
[ #       o   o ]
[ #   $   P   P ]
[     $   o   o ]


Move: 18
[ @   R   R   * ]
[ @   R   R   * ]
[ #   $   o   o ]
[ #   $   P   P ]
[         o   o ]


Move: 19
[ @   R   R   * ]
[ @   R   R   * ]
[ #   $   o   o ]
[ #   $   P   P ]
[ o           o ]


Move: 20
[ @   R   R   * ]
[ @   R   R   * ]
[ #   $   o   o ]
[ #   $   P   P ]
[ o   o         ]


Move: 21
[ @   R   R   * ]
[ @   R   R   * ]
[ #   $   o   o ]
[ #   $         ]
[ o   o   P   P ]


Move: 22
[ @   R   R   * ]
[ @   R   R   * ]
[ #   $       o ]
[ #   $       o ]
[ o   o   P   P ]


Move: 23
[ @   R   R   * ]
[ @   R   R   * ]
[ #       $   o ]
[ #       $   o ]
[ o   o   P   P ]


Move: 24
[ @   R   R   * ]
[ @   R   R   * ]
[     #   $   o ]
[     #   $   o ]
[ o   o   P   P ]


Move: 25
[     R   R   * ]
[     R   R   * ]
[ @   #   $   o ]
[ @   #   $   o ]
[ o   o   P   P ]


Move: 26
[ R   R       * ]
[ R   R       * ]
[ @   #   $   o ]
[ @   #   $   o ]
[ o   o   P   P ]


Move: 27
[ R   R   *     ]
[ R   R   *     ]
[ @   #   $   o ]
[ @   #   $   o ]
[ o   o   P   P ]


Move: 28
[ R   R   *   o ]
[ R   R   *     ]
[ @   #   $     ]
[ @   #   $   o ]
[ o   o   P   P ]


Move: 29
[ R   R   *   o ]
[ R   R   *   o ]
[ @   #   $     ]
[ @   #   $     ]
[ o   o   P   P ]


Move: 30
[ R   R   *   o ]
[ R   R   *   o ]
[ @   #       $ ]
[ @   #       $ ]
[ o   o   P   P ]


Move: 31
[ R   R       o ]
[ R   R       o ]
[ @   #   *   $ ]
[ @   #   *   $ ]
[ o   o   P   P ]


Move: 32
[     R   R   o ]
[     R   R   o ]
[ @   #   *   $ ]
[ @   #   *   $ ]
[ o   o   P   P ]


Move: 33
[ @   R   R   o ]
[ @   R   R   o ]
[     #   *   $ ]
[     #   *   $ ]
[ o   o   P   P ]


Move: 34
[ @   R   R   o ]
[ @   R   R   o ]
[ #       *   $ ]
[ #       *   $ ]
[ o   o   P   P ]


Move: 35
[ @   R   R   o ]
[ @   R   R   o ]
[ #   o   *   $ ]
[ #       *   $ ]
[ o       P   P ]


Move: 36
[ @   R   R   o ]
[ @   R   R   o ]
[ #   o   *   $ ]
[ #   o   *   $ ]
[         P   P ]


Move: 37
[ @   R   R   o ]
[ @   R   R   o ]
[ #   o   *   $ ]
[ #   o   *   $ ]
[ P   P         ]


Move: 38
[ @   R   R   o ]
[ @   R   R   o ]
[ #   o       $ ]
[ #   o   *   $ ]
[ P   P   *     ]


Move: 39
[ @   R   R   o ]
[ @   R   R   o ]
[ #   o         ]
[ #   o   *   $ ]
[ P   P   *   $ ]


Move: 40
[ @   R   R   o ]
[ @   R   R   o ]
[ #           o ]
[ #   o   *   $ ]
[ P   P   *   $ ]


Move: 41
[ @           o ]
[ @   R   R   o ]
[ #   R   R   o ]
[ #   o   *   $ ]
[ P   P   *   $ ]


Move: 42
[ @   o         ]
[ @   R   R   o ]
[ #   R   R   o ]
[ #   o   *   $ ]
[ P   P   *   $ ]


Move: 43
[ @   o   o     ]
[ @   R   R     ]
[ #   R   R   o ]
[ #   o   *   $ ]
[ P   P   *   $ ]


Move: 44
[ @   o   o   o ]
[ @   R   R     ]
[ #   R   R     ]
[ #   o   *   $ ]
[ P   P   *   $ ]


Move: 45
[ @   o   o   o ]
[ @   R   R   $ ]
[ #   R   R   $ ]
[ #   o   *     ]
[ P   P   *     ]


Move: 46
[ @   o   o   o ]
[ @   R   R   $ ]
[ #   R   R   $ ]
[ #   o       * ]
[ P   P       * ]


Move: 47
[ @   o   o   o ]
[ @   R   R   $ ]
[ #   R   R   $ ]
[ #           * ]
[ P   P   o   * ]


Move: 48
[ @   o   o   o ]
[ @           $ ]
[ #   R   R   $ ]
[ #   R   R   * ]
[ P   P   o   * ]


Move: 49
[ @       o   o ]
[ @       o   $ ]
[ #   R   R   $ ]
[ #   R   R   * ]
[ P   P   o   * ]


Move: 50
[     @   o   o ]
[     @   o   $ ]
[ #   R   R   $ ]
[ #   R   R   * ]
[ P   P   o   * ]


Move: 51
[ #   @   o   o ]
[ #   @   o   $ ]
[     R   R   $ ]
[     R   R   * ]
[ P   P   o   * ]


Move: 52
[ #   @   o   o ]
[ #   @   o   $ ]
[ R   R       $ ]
[ R   R       * ]
[ P   P   o   * ]


Move: 53
[ #   @   o   o ]
[ #   @       $ ]
[ R   R   o   $ ]
[ R   R       * ]
[ P   P   o   * ]


Move: 54
[ #   @       o ]
[ #   @   o   $ ]
[ R   R   o   $ ]
[ R   R       * ]
[ P   P   o   * ]


Move: 55
[ #   @   o     ]
[ #   @   o   $ ]
[ R   R   o   $ ]
[ R   R       * ]
[ P   P   o   * ]


Move: 56
[ #   @   o   $ ]
[ #   @   o   $ ]
[ R   R   o     ]
[ R   R       * ]
[ P   P   o   * ]


Move: 57
[ #   @   o   $ ]
[ #   @   o   $ ]
[ R   R   o   * ]
[ R   R       * ]
[ P   P   o     ]


Move: 58
[ #   @   o   $ ]
[ #   @   o   $ ]
[ R   R   o   * ]
[ R   R       * ]
[ P   P       o ]


Move: 59
[ #   @   o   $ ]
[ #   @   o   $ ]
[ R   R       * ]
[ R   R       * ]
[ P   P   o   o ]


Move: 60
[ #   @   o   $ ]
[ #   @   o   $ ]
[     R   R   * ]
[     R   R   * ]
[ P   P   o   o ]


Move: 61
[     @   o   $ ]
[     @   o   $ ]
[ #   R   R   * ]
[ #   R   R   * ]
[ P   P   o   o ]


Move: 62
[ @       o   $ ]
[ @       o   $ ]
[ #   R   R   * ]
[ #   R   R   * ]
[ P   P   o   o ]


Move: 63
[ @       o   $ ]
[ @   o       $ ]
[ #   R   R   * ]
[ #   R   R   * ]
[ P   P   o   o ]


Move: 64
[ @   o       $ ]
[ @   o       $ ]
[ #   R   R   * ]
[ #   R   R   * ]
[ P   P   o   o ]


Move: 65
[ @   o   $     ]
[ @   o   $     ]
[ #   R   R   * ]
[ #   R   R   * ]
[ P   P   o   o ]


Move: 66
[ @   o   $   * ]
[ @   o   $   * ]
[ #   R   R     ]
[ #   R   R     ]
[ P   P   o   o ]


Move: 67
[ @   o   $   * ]
[ @   o   $   * ]
[ #       R   R ]
[ #       R   R ]
[ P   P   o   o ]


Move: 68
[ @   o   $   * ]
[ @       $   * ]
[ #       R   R ]
[ #   o   R   R ]
[ P   P   o   o ]


Move: 69
[ @       $   * ]
[ @       $   * ]
[ #   o   R   R ]
[ #   o   R   R ]
[ P   P   o   o ]


Move: 70
[     @   $   * ]
[     @   $   * ]
[ #   o   R   R ]
[ #   o   R   R ]
[ P   P   o   o ]


Move: 71
[ #   @   $   * ]
[ #   @   $   * ]
[     o   R   R ]
[     o   R   R ]
[ P   P   o   o ]


Move: 72
[ #   @   $   * ]
[ #   @   $   * ]
[ o   o   R   R ]
[         R   R ]
[ P   P   o   o ]


Move: 73
[ #   @   $   * ]
[ #   @   $   * ]
[ o   o   R   R ]
[ P   P   R   R ]
[         o   o ]


Move: 74
[ #   @   $   * ]
[ #   @   $   * ]
[ o   o   R   R ]
[ P   P   R   R ]
[ o           o ]


Move: 75
[ #   @   $   * ]
[ #   @   $   * ]
[ o   o   R   R ]
[ P   P   R   R ]
[ o   o         ]


Move: 76
[ #   @   $   * ]
[ #   @   $   * ]
[ o   o         ]
[ P   P   R   R ]
[ o   o   R   R ]


Move: 77
[ #   @   $   * ]
[ #   @   $   * ]
[ o           o ]
[ P   P   R   R ]
[ o   o   R   R ]


Move: 78
[ #   @   $   * ]
[ #   @   $   * ]
[         o   o ]
[ P   P   R   R ]
[ o   o   R   R ]


Move: 79
[ #   @   $   * ]
[ #   @   $   * ]
[ P   P   o   o ]
[         R   R ]
[ o   o   R   R ]


Move: 80
[ #   @   $   * ]
[ #   @   $   * ]
[ P   P   o   o ]
[ o       R   R ]
[ o       R   R ]


Move: 81
[ #   @   $   * ]
[ #   @   $   * ]
[ P   P   o   o ]
[ o   R   R     ]
[ o   R   R     ]

SOLVED
```
