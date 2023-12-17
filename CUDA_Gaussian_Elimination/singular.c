// Consider the lex term order with x > y > z on the ring Q[x, y, z]

LIB "teachstd.lib";

ring r = 0,(x,y,z),dp;

// f1 = 2x^2 + y
poly f1 = 2x2 + y;

// f2 = 3xy2 − xy
poly f2 = 3xy2 - xy;

//f3 = 4y3 − 1
poly f3 = 4y3 - 1;

// Spoly(f1, f2)
poly a = spoly(f1, f2);
a;

// why in the book has (1/3)x2y + (1/3)y3
// but here has 2/3x2y+y3