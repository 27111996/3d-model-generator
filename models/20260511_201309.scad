module leg(size = 20, thickness = 2) {
    difference() {
        cube([size, size, 100], center=true);
        move_up(thickness)(cylinder(r1=thickness/2, h=size-thickness*2));
    }
}

module seat(width = 30, depth = 20, height = 5) {
    difference() {
        cube([width, depth, height], center=true);
        translate([width/2, 0, height/2]) cylinder(r1=width/2+1, r2=width/2[10D[K
r2=width/2+2, h=depth-height);
    }
}

leg4(offset = [30, -30, 30, -30], legsCount = 4, thickness = 5) {
    for(i = [0:legsCount]) {
        leg(size = 20 + offset[i]);
    }
}

chair() {
    scale(1.2) leg4();
    move_down(130) seat();
}