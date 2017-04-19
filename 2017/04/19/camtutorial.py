import rhinoscriptsyntax as rs
import math

# Range of degrees from 0 to 360 by delta
delta = 15
degrees = range(0,360+delta,delta)

# Create a sin function that goes from 0 to h
# in the interval of 0 to 180 degrees and goes back to 0 from 180 to 360.
h = 15
L = []

for alpha in range(-90,270+delta,delta): #Translates the sin function horizontally
    radian_alpha = alpha * math.pi / 180
    L.append((round(math.sin(radian_alpha),4) + 1 )* h/2) # Adjust the sin function vertically

# Base radius of the cam 
R = 30

# Radius of the follower
r = 5

# Rotation center of the cam
p_zero = (0,0,0)

# Drawing colors
red =(255,0,0)
blue = (0,0,255)
magenta = (255,0,255)
yellow = (255,255,0)
green = (0,255,0)

# Lists of points and lines
points = []
profile_line = []
radial_line = []
tangent_points =[]

rs.AddCircle(p_zero,R)

# Draw lines and circles for each degree with the corresponding length
for (i,degree) in enumerate(degrees[:-1]):
    # Draw a line from the rotation center to the position of the follower
    p_end = rs.Polar(p_zero, degree,R+r+L[i])
    radial_line.append(rs.AddLine(p_zero,p_end))
    
    # Save the position of the follower's center for drawing the motion of it
    points.append(p_end)
    
    #Draw the follower
    circle = rs.AddCircle(p_end,r)
    
    # Suppose the initial contact point is the intersection of the follower and the radius of the cam
    p_tangent = rs.Polar(p_zero, degree,R+L[i])
    tangent_points.append(p_tangent)
    
    #Calc the contact point of the next follower position
    p_tangent_next = rs.Polar(p_zero, degrees[i+1],R+L[i+1])
    
    # Draw lines connecting the supposed contact points (profile_line)
    profile_line.append(rs.AddLine(p_tangent,p_tangent_next))
    rs.ObjectColor(profile_line[i], color=red)
    
    # Draw tangent lines at the supposed contact points
    p_end = rs.Polar(p_tangent, degree+90,10)
    rs.ObjectColor(rs.AddLine(p_tangent,p_end),blue)
    p_end = rs.Polar(p_tangent, degree-90,10)
    rs.ObjectColor(rs.AddLine(p_tangent,p_end),blue)

# Draw the curve of the motion of the follower
points.append(points[0])
rs.AddInterpCurve(points, degree=3, knotstyle=3)

# Draw the curve of the original supposed contact points to show the difference
tangent_points.append(tangent_points[0])
rs.ObjectColor(rs.AddInterpCurve(tangent_points, degree=3, knotstyle=3),yellow)

# Calculate a new supposed contact points
points = []

for i in xrange(len(degrees)-1):
    # Calculate the difference(angle) between the radial lines and profile lines
    alpha = rs.Angle2(radial_line[i],profile_line[i])[0]
    beta = rs.Angle2(radial_line[i],profile_line[i-1])[0]
    
    # Calculate the angle were the new contact point is suppossed to be
    gamma = 90 - (alpha+beta)/2
    
    # Draw a line and store the end point (new supposed contact point)
    p_start = rs.Polar(p_zero, degrees[i],R+L[i]+r)
    p_end = rs.Polar(p_start, degrees[i]+180-gamma,r)
    rs.ObjectColor(rs.AddLine(p_start,p_end), color=green)
    points.append(p_end)

# Draw the curve of the cam (interpolating through the suppossed contact points)
points.append(points[0])
rs.ObjectColor(rs.AddInterpCurve(points, degree=3, knotstyle=3),magenta)