module chair() {
    // Define leg dimensions
    float leg_width = 20;
    float leg_height = 50;

    // Define seat dimensions
    float seat_length = 30;
    float seat_width = 15;
    float seat_height = 10;

    // Define backrest dimensions
    float backrest_height = 20;
    float backrest_width = seat_width;
    float backrest_depth = 20;

    difference() {
        // Create legs
        cube([leg_width, leg_height, 10], center=true); // Center the legs [K
for easier positioning

        // Create seat
        cube([seat_length, seat_width, seat_height]);
        move([0, -seat_width/2, seat_height]) rotateY(90) cube([seat_width,[17D[K
cube([seat_width, seat_length, seat_height]); // Mirror the first seat half[4D[K
half for the second one

        // Create backrest
        cube([backrest_width, backrest_height, backrest_depth]);
        move([-backrest_width/2, 0, -backrest_depth]) rotateY(90) scale([1,[9D[K
scale([1, -1, 1]) cube([backrest_width, backrest_height, backrest_depth]); [K
// Mirror the first backrest half for the second one
    }
}

chair();