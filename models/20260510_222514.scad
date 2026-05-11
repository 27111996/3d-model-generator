Here is a simple example of a chair with 4 legs in OpenSCAD:


module chair(leg_length = 50, seat_width = 100, seat_depth = 30) {
    difference(){
        cube(h = leg_length, center = true); // Front leg
        translate([0, leg_length, 0]) rotate([90, 0]) cube(h = leg_length, [K
center = true); // Right leg
        translate([-100/2, leg_length, 0]) rotate([90, 0]) cube(h = leg_len[7D[K
leg_length, center = true); // Back leg
        translate([100/2, leg_length, 0]) rotate([90, 0]) cube(h = leg_leng[8D[K
leg_length, center = true); // Left leg

        translate([0, (leg_length + seat_depth)/2, 0]) square(size = seat_w[6D[K
seat_width, center = true); // Seat
    }
}

chair();


This code creates a chair with four legs of length `leg_length`, a seat of [K
width `seat_width` and depth `seat_depth`. The origin is located at the fro[3D[K
front-left corner of the seat. The chair is centered around the origin, so [K
adjust the position of the legs if you want to place it in a different posi[4D[K
position.