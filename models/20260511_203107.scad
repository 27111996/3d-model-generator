cube([20,20,6], center=true); // seat
cylinder(h=6, r1=8, r2=8, $fn=32); // backrest

for(i = [0,1,2,3]){
    translate((-20+i*5, 0, -3))
        cylinder(h=6, r1=2, r2=2, $fn=32); // legs
}