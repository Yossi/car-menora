$fa = 1;
$fs = 0.4;

epsilon = 0.001;
slop = 0.15;

//all measurements in mm

inner_pipe_diameter = 15.15;
outer_pipe_diameter = 21.4 - slop;
pipe_wall_thickness = 3.3;

lip_thickness = 2;
plug_thickness = 5;

washer_height = 1;
washer_diameter = 11.53 + slop;
washer_hole_diameter = 4.88;

blob_thickness = 2;

bottom_total_height = lip_thickness + plug_thickness;

module bottom(){
    difference(){
        union(){
            // bottom lip
            color("Orange")
            cylinder(h = lip_thickness, r = inner_pipe_diameter/2 + pipe_wall_thickness*.8);

            // plug
            translate([0,0,lip_thickness-epsilon])
            cylinder(h = plug_thickness, r = inner_pipe_diameter/2 - epsilon);
        }

        // washer
        translate([0,0,lip_thickness+plug_thickness-washer_height])
        color("Red")
        cylinder(h = washer_height + epsilon, r = washer_diameter/2);

        // central column
        translate([0,0,-epsilon])
        color("Purple")
        cylinder(h = lip_thickness+plug_thickness, r = washer_hole_diameter/2 + 1);

        // wire passthrough
        translate([0,-1,-epsilon])
        cube([washer_diameter/2 + 1, 2, bottom_total_height+epsilon]);

        // under washer solder blob clearance
        rotate([0,0,-20])
        translate([0,0,lip_thickness+plug_thickness-blob_thickness+epsilon])
        rotate_extrude(angle=40)
        polygon([
                    [washer_hole_diameter/2, blob_thickness],
                    [washer_diameter/2, blob_thickness],
                    [washer_diameter/2, 0],
                    [washer_hole_diameter/2, 0]
                ]);

    }
}

bottom();