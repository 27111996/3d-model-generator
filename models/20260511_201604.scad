cube([20,20,5], center=true);
for(i=[0:3]){
 translate((-20+i*10,0,4))
 cube([8,8,3],center=true);
}
cylinder(h=4,r1=8,r2=6.5, $fn = 60);
for(i=[0:3]){
 translate((-10+i*9.5,7,-3))
 cylinder(h=3,r=1, $fn = 60);
}
cylinder(h=20,r1=4,r2=8, $fn = 60);
for(i=[0:3]){
 translate((-9.5+i*9.5,2,-1))
 cylinder(h=1.5,r=0.75, $fn = 60);
}
translate((0,0,-4))
cylinder(h=1.5,r1=3,r2=2.5, $fn = 60);
for(i=[0:3]){
 translate((-9.5+i*9.5,18,-1))
 cylinder(h=1.5,r=0.75, $fn = 60);
}
translate((0,20,-4))
cylinder(h=1.5,r1=3,r2=2.5, $fn = 60);