module chair() {
    difference() {
        cube([20, 20, 3], center = true); // seat base
        translate([0, 0, -15]) rotate(90) cube([20, 2, 20], center = true);[6D[K
true); // seat back
        translate([-6, 0, -18]) rotate(45) cylinder(h=20, r1=3, r2=5); // f[1D[K
front left leg
        translate([-6, 0, -18]) rotate(-45) cylinder(h=20, r1=3, r2=5); // [K
front right leg
        translate([6, 0, -18]) rotate(45) cylinder(h=20, r1=3, r2=5); // ba[2D[K
back left leg
        translate([6, 0, -18]) rotate(-45) cylinder(h=20, r1=3, r2=5); // b[1D[K
back right leg
    }
}

chair();