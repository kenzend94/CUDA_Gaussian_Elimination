// Singular 

LIB "teachstd.lib";
// Input: f, F = {f1, . . . , fs}, term order >
//Consider the lex term order with x > y > z on the ring Q[x, y, z].

ring r = 0, (x,y,z), lp;

// Given F = {f1 = 2x2 + y, f2 = 3xy2 − xy, f3 = 4y3 − 1}

poly f1 = 2*x2 + y;
poly f2 = 3*x*y2 - x*y;
poly f3 = 4*y3 - 1;

ideal I = f1,f2,f3;

// calculate S-poly(f1, f2) = f4

poly f4 = spoly(f1,f2);
f4;

poly f5 = 1/3*x2*y + 1/2*y3;
f5;

// reduce f5


// i got result as 2/3x2y + y3 while 1/3x2y + 1/2y3 is expected


// Output: A matrix M representing f −−−−−→+ r by f1, . . . , fs
