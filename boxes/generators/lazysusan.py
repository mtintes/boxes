# Copyright (C) 2013-2016 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *


class LazySusan(Boxes):
    """Box for storing tipable things on a lazy susan"""

    ui_group = "FlexBox"

    def __init__(self) -> None:
        Boxes.__init__(self)

        self.addSettingsArgs(edges.FingerJointSettings)
        self.addSettingsArgs(edges.FlexSettings)

        self.buildArgParser(outside="FALSE",h=110,)
        self.argparser.add_argument(
            "--inside_radius", action="store", type=float, default=40,
            help="inside radius of the lazy susan.")
        self.argparser.add_argument(
            "--outside_radius", action="store", type=float, default=280,
            help="outside radius of the lazy susan")
        self.argparser.add_argument(
            "--angle", action="store", type=float, default=70,
            help="angle of the lazy susan. If outside is false it's the angle between the inside of the endcap wall")
        self.argparser.add_argument(
                "--handle", action="store", type=bool, default='False', 
                help="Draw an indent on the wall to use ase handle")
        self.argparser.add_argument(
            "--top",  action="store", type=str, default="hole",
            choices=["hole", "lid", "closed",],
            help="style of the top and lid")

    def drawfloor(self, angle=None, inside_radius=None, outside_radius=None):
        with self.saved_context():
            self.moveTo(inside_radius, 0)
            self.moveArc(90)
            self.polyline(0, (angle, inside_radius))

        with self.saved_context():
            self.moveTo(outside_radius, 0)
            self.moveArc(90)
            self.polyline(0, (angle, outside_radius))
            self.polyline(0, 90)
            self.edges["f"](outside_radius-inside_radius)

        with self.saved_context():
            self.moveTo(inside_radius, 0)
            self.edges["f"](outside_radius-inside_radius)

    def drawWall(self, length, height, edges):
        """Draw a wall with the given width, height, edges and label."""
        with self.saved_context():
            self.moveTo(0, 0)
            self.edges[edges[0]](length)
            self.corner(90)
            self.edges[edges[1]](height)
            self.corner(90)
            self.edges[edges[2]](length)
            self.corner(90)
            self.edges[edges[3]](height)

    def drawFlexWall(self, length, height,thickness):
        """Draw a wall with the given width, height, edges and label."""
        with self.saved_context():
            self.moveTo(0, 0)
            self.edges["e"](thickness)
            self.edges["X"](length-2*thickness, h=height+thickness)
            self.edges["e"](thickness)
            self.corner(90)
            self.edges["F"](height+thickness, h=length)
            self.corner(90)
            self.edges["e"](length)
            self.corner(90)
            self.edges["F"](height+thickness, h=length)



    def render(self):
        if self.outside:
            o=self.thickness
            angle_diminution= 2*self.thickness/(self.inside_radius+self.thickness)*180/math.pi  
        else:
            o=0
            angle_diminution=0
        if self.outside and (self.top=='lid' or self.top=='close'):
            top=self.thickness
        else:
            top=0
##  The drawing of the file start here

        angle, inside_radius, outside_radius, h = self.angle, self.inside_radius+o, self.outside_radius-o, self.h-top-o
        t = self.thickness

        self.moveTo(0, 5)
        self.drawfloor(angle-angle_diminution, inside_radius, outside_radius)
        self.moveTo(outside_radius+5, 0)

        # #flex wall for outside
        outside_wall = angle * (math.pi / 180) * outside_radius + 2*t-2*o
        self.drawFlexWall(outside_wall, h,t)
        if self.handle:
            with self.saved_context():
                self.moveTo(outside_wall/2-10,h+t+0.05)
                self.curveTo(0,-15,20,-15,20,0)




        #flex wall for inside
        self.moveTo(outside_wall+10, 0)
        inside_wall = angle * (math.pi / 180) * (inside_radius-t) + 2*t-2*o
        self.drawFlexWall(inside_wall, h,t)

        #solid endcap walls
        self.moveTo(inside_wall+10,0)
        self.drawWall(outside_radius-inside_radius, h+t, "Ffef")

        self.moveTo(outside_radius-inside_radius+10, 0)
        self.drawWall(outside_radius-inside_radius, h+t, "Ffef")
