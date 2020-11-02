$fa = 1;
$fs = 0.4;

epsilon = 0.001;

//all measurements in mm

inner_pipe_diameter = 15.5;
outer_pipe_diameter = 21.4;
pipe_wall_thickness = 3.06;
tube_wall_thickness = 3;
cap_wall_thickness = 2;
funnel_height = 4;

board_short_way = 11.4;
board_long_way = 22.1;
board_thickness = 1.6;

board_clearance = 4;
component_width = 8.43;
sideA_clearance = 1.81;
sideB_clearance = 1.16;

led_main_diameter = 5;
led_base_diameter = 5.7;

/*difference(){*/

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
                    r1=led_base_diameter/2,
                    r2=inner_pipe_diameter/2 - tube_wall_thickness
                );
            }

            //simple tube
            color("Grey")
            difference() {
                cylinder(h=funnel_height + board_long_way - epsilon,
                         r=inner_pipe_diameter/2);
                translate([0, 0, -epsilon])
                cylinder(h=board_short_way + board_long_way + epsilon,
                         r=(inner_pipe_diameter/2) - tube_wall_thickness);
            }
        }
        
        //board
        translate([
            board_thickness*.75,
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
    }


    // end cap
    difference(){
        color("Pink")
        cylinder(
            h=cap_wall_thickness*2 - epsilon,
            r=inner_pipe_diameter/2 + pipe_wall_thickness + cap_wall_thickness
        );
        translate([0, 0, -epsilon])
        cylinder(
            h=cap_wall_thickness*(2+epsilon),
            r=inner_pipe_diameter/2 - cap_wall_thickness
        );
        translate([0, 0, cap_wall_thickness])
        cylinder(
            h=cap_wall_thickness,
            r=inner_pipe_diameter/2 + pipe_wall_thickness
        );
    }
}

/*//cross section
translate([0, 0, -epsilon])
cube([15,15,40]);
}*/
