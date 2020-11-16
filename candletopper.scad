$fa = 1;
$fs = 0.4;

epsilon = 0.001;
slop = 0.04;

//all measurements in mm

inner_pipe_diameter = 15.15;
outer_pipe_diameter = 21.4;
pipe_wall_thickness = 3.3;
tube_wall_thickness = 2.25;
cap_wall_thickness = 2;
funnel_height = 2;

board_short_way = 11.4 + slop;
board_long_way = 22.1;
board_thickness = 1.6 + slop;

solder_pads = 3.5;
blob_thickness = 1;
board_clearance = 4;
component_width = 8.43;
sideA_clearance = 1.81;
sideB_clearance = 1.16;
board_offset_multiplier = .55;

led_main_diameter = 5;
led_base_diameter = 5.7;

top_washer_height = 1;
top_washer_diameter = 11.53;


difference(){

//color("DarkSlateGray")
union(){
    // inside part
    difference(){
        //un notched part

        union(){
            //funnel
            color("Yellow")
            difference() {
                cylinder(
                    h=funnel_height - epsilon,
                    r=inner_pipe_diameter/2 - epsilon
                );
                translate([0, 0, -epsilon])
                cylinder(
                    h=funnel_height + epsilon,
                    r1=led_base_diameter/2 + slop,
                    r2=inner_pipe_diameter/2 - tube_wall_thickness
                );
            }

            //simple tube
            color("Grey")
            difference() {
                cylinder(h=funnel_height + board_long_way + top_washer_height - epsilon,
                         r=inner_pipe_diameter/2);
                translate([0, 0, -epsilon])
                cylinder(h=funnel_height + board_long_way + epsilon,
                         r=(inner_pipe_diameter/2) - tube_wall_thickness);
            }
        }

        // board
        translate([
            board_thickness * board_offset_multiplier,
            -board_short_way/2,
            funnel_height
        ])
        union(){
            color("LightBlue")
            cube([
                board_thickness,
                board_short_way,
                board_long_way
            ]);

            // solder blobs
            translate([
                board_thickness - epsilon,
                0,
                board_long_way-solder_pads])
            color("Orange")
            rotate([90,90,180])
            linear_extrude(height=board_short_way)
            polygon([
                [blob_thickness / 2, 0],
                [-blob_thickness / 2, -blob_thickness],
                [-solder_pads, -blob_thickness],
                [-solder_pads, 0]
            ]);

            // components
            translate([
                -board_clearance + board_thickness,
                sideA_clearance,
                2
            ])
            color("Red")
            cube([
                board_clearance - epsilon,
                component_width,
                board_long_way - 4
            ]);
        }

        // board clearance
        translate([
            board_thickness * board_offset_multiplier,
            -board_short_way / 2,
            funnel_height + board_long_way - epsilon
        ])
        color("Blue")
        cube([
            board_thickness + blob_thickness,
            board_short_way,
            top_washer_height + epsilon
        ]);

        // top washer
        translate([0, 0, funnel_height + board_long_way - epsilon])
        cylinder(h=top_washer_height + epsilon,
                 r=top_washer_diameter/2);

        // wire passthrough
        translate([
            top_washer_diameter/2 - 1,
            -1.25,
            funnel_height + board_long_way - 4
        ])
        cube([2, 2.5, 5]);
    }


    // end cap
    difference(){
        // slab
        color("Pink")
        cylinder(
            h=cap_wall_thickness*2 - epsilon,
            r=inner_pipe_diameter/2 + pipe_wall_thickness + cap_wall_thickness
        );
        // space for the LED funnel
        translate([0, 0, -epsilon])
        cylinder(
            h=cap_wall_thickness*(2+epsilon),
            r=inner_pipe_diameter/2 - cap_wall_thickness + epsilon
        );
        // outside trough for pipe wall
        translate([0, 0, cap_wall_thickness])
        cylinder(
            h=cap_wall_thickness,
            r1=inner_pipe_diameter/2 + pipe_wall_thickness,
            r2=inner_pipe_diameter/2 + pipe_wall_thickness + cap_wall_thickness/2
        );
    }
}

//cross section
// translate([0, 0, -epsilon]) cube([15,15,20]);
}
