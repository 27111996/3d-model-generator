module chair(leg_length = 100, seat_width = 120, seat_depth = 30, backrest_[9D[K
backrest_height = 60) {
    difference() {
        cube([seat_width, leg_length, seat_depth], center=true); // Seat
        cube([seat_width, backrest_height, seat_depth], translate=([0, leg_[4D[K
leg_length - backrest_height, 0])); // Backrest

        for(i = [1,2,3,4]) {
            minkowski(legs)[i] = cube([20, leg_length, 20]);
            translate(legs[i], origin, [(-seat_width/2 + i*30), 0, -(seat_d[8D[K
-(seat_depth/2)]);
        }

        minkowski(union) {
            for(i = legs) {
                union() {
                    translate(i, origin, [0, leg_length-5, 0]) cube([30, 5,[2D[K
5, 30]); // Footrest
                    i;
                }
            }
        }
    }
}
chair();