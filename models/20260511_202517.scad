module chair() {
    // Leg dimensions
    float leg_height = 20;
    float leg_width = 2;
    float leg_thickness = 1;

    // Seat dimensions
    float seat_width = 30;
    float seat_depth = 15;
    float seat_height = 5;

    // Backrest dimensions
    float backrest_height = 20;
    float backrest_width = 15;
    float backrest_thickness = 1;

    difference() {
        cube([seat_width, seat_depth, seat_height], center=true);
        translate([0, -seat_height/2, 0]) rotateY(90) cube([seat_width, sea[3D[K
seat_depth, backrest_height], center=true);

        // Legs
        for(i = [0:3]) {
            translate(vec3d(5 + i*(seat_width/2 - 5), leg_height, 0)) {
                cube([leg_width, leg_height, leg_thickness], center=true);
                cylinder(h = leg_height, r1 = leg_width/2, r2 = leg_width/2[11D[K
leg_width/2 - leg_thickness);
            }
        }
    }
}

chair();