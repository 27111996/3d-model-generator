module chair_legs(size) {
    // Create the leg body
    cylinder(d = size*2, h = size/2, center = true);

    // Create the top part of the leg
    cylinder(d = size*1.5, h = size/4, center = true);

    // Create the bottom part of the leg
    cylinder(d = size*0.8, h = size/4, center = true);
}

module chair(size) {
    // Create the base of the chair
    cylinder(d = size*2, h = size/2, center = true);

    // Create the legs of the chair
    translate([size/4, size/2, -size/2]) {
        rotate([90, 0, 0]) {
            chair_legs(size);
        }
    }

    translate([-size/4, size/2, -size/2]) {
        rotate([90, 180, 0]) {
            chair_legs(size);
        }
    }

    translate([0, size/2, -size/2]) {
        rotate([0, 0, 180]) {
            chair_legs(size);
        }
    }

    translate([-size/4, -size/2, -size/2]) {
        rotate([90, 0, 0]) {
            chair_legs(size);
        }
    }

    translate([size/4, -size/2, -size/2]) {
        rotate([90, 180, 0]) {
            chair_legs(size);
        }
    }

    translate([0, -size/2, -size/2]) {
        rotate([0, 0, 180]) {
            chair_legs(size);
        }
    }
}

// Example usage
chair(size=50);