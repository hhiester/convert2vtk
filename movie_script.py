# Restore the template session to create movie from
RestoreSession("/panfs/storage.local/coaps/home/ndc08/code/converter/todd_roms_july/imgs/final.session", 0 )

# Make all the views for the prep phase of the movie (slowly zoom in)
v0 = View3DAttributes()
v0.viewNormal = (0, 0, 1)
v0.focus = (275.329, 29.2667, -7.50835)
v0.viewUp = (0, 1, 0)
v0.viewAngle = 30
v0.parallelScale = 7.89321
v0.nearPlane = -15.7864
v0.farPlane = 15.7864
v0.imagePan = (0, 0)
v0.imageZoom = 1
v0.perspective = 1
v0.eyeAngle = 2
v0.centerOfRotationSet = 0
v0.centerOfRotation = (275.329, 29.2667, -7.50835)
v0.axis3DScaleFlag = 0
v0.axis3DScales = (1, 1, 1)
v0.shear = (0, 0, 1)


v1 = View3DAttributes()
v1.viewNormal = (-0.00756598, -0.670641, 0.741743)
v1.focus = (275.329, 29.2667, -7.50835)
v1.viewUp = (-0.00609591, 0.741782, 0.670614)
v1.viewAngle = 30
v1.parallelScale = 7.89321
v1.nearPlane = -15.7864
v1.farPlane = 15.7864
v1.imagePan = (0.0126309, -0.355923)
v1.imageZoom = 3.6
v1.perspective = 1
v1.eyeAngle = 2
v1.centerOfRotationSet = 0
v1.centerOfRotation = (275.329, 29.2667, -7.50835)
v1.axis3DScaleFlag = 0
v1.axis3DScales = (1, 1, 1)
v1.shear = (0, 0, 1)


prep_views = (v0, v1)

# Save Attributes
output_img = "/panfs/storage.local/coaps/home/ndc08/code/converter/todd_roms_july/imgs/"
s = SaveWindowAttributes()
s.format = s.JPEG
s.outputToCurrentDirectory = 0
s.outputDirectory = output_img
s.family = 1   # 1 if want Visit to automatically add 000, 001, to the end of file
s.fileName = "frame"
s.resConstraint = 0
s.width, s.height = 1680, 1050
s.screenCapture = 0
s.stereo = 0
SetSaveWindowAttributes(s)

# Fist for loop for the bathymetry and *prepping the viewer*
size = len( prep_views )
x_prep = []
for i in range( size ):
    x_prep += [float(i) / float( size-1 )]


prep_states = 60
attr = GetAnnotationAttributes()
p = PseudocolorAttributes()
p.opacity = 0
SetPlotOptions(p)
for i in xrange( prep_states ):
    if i >= 18:
        opacity = float(i-18) / float(prep_states-19)
        p.opacity = opacity
        print "\n\n OPACITY = ", p.opacity, "\n"
        SetPlotOptions(p)
    if p.opacity >= .50:
        attr.legendInfoFlag = 1
        SetAnnotationAttributes(attr)
    
    SetSaveWindowAttributes(s)
    t = float(i) / float(prep_states - 1)
    c = EvalCubicSpline(t, x_prep, prep_views)  
    SetView3D(c)
    SaveWindow()

t = ThresholdAttributes()
transition_states = prep_states/2
for i in xrange(transition_states):
    if i >= transition_states/3:
        t.lowerBounds = (14)
        t.upperBounds = (24)
        p.minFlag = 1
        p.min = 14
        p.maxFlag = 1
        p.max = 24
        SetOperatorOptions(t)
        SetPlotOptions(p)
        DrawPlots()
    if i >= 2*(transition_states/3):
        attr.axes3D.visible = 0
        attr.axes3D.bboxFlag = 0
        SetAnnotationAttributes(attr)
    SaveWindow()

# Make all the views for the pseudo color temp phase (pan around)
# begin from where we left off in the previous loop
v2 = v1

v3 = View3DAttributes()
v3.viewNormal = (0.0013826, -0.833921, 0.551882)
v3.focus = (275.329, 29.2667, -7.50835)
v3.viewUp = (0.000209106, 0.551882, 0.833922)
v3.viewAngle = 30
v3.parallelScale = 7.89321
v3.nearPlane = -15.7864
v3.farPlane = 15.7864
v3.imagePan = (0.0191257, -0.412748)
v3.imageZoom = 3.6
v3.perspective = 1
v3.eyeAngle = 2
v3.centerOfRotationSet = 0
v3.centerOfRotation = (275.329, 29.2667, -7.50835)
v3.axis3DScaleFlag = 0
v3.axis3DScales = (1, 1, 1)
v3.shear = (0, 0, 1)

v4 = View3DAttributes()
v4.viewNormal = (-0.296521, -0.762542, 0.574983)
v4.focus = (275.329, 29.2667, -7.50835)
v4.viewUp = (0.296951, 0.4986, 0.814382)
v4.viewAngle = 30
v4.parallelScale = 7.89321
v4.nearPlane = -15.7864
v4.farPlane = 15.7864
v4.imagePan = (0.0339472, -0.406979)
v4.imageZoom = 3.5
v4.perspective = 1
v4.eyeAngle = 2
v4.centerOfRotationSet = 0
v4.centerOfRotation = (275.329, 29.2667, -7.50835)
v4.axis3DScaleFlag = 0
v4.axis3DScales = (1, 1, 1)
v4.shear = (0, 0, 1)


v5 = View3DAttributes()
v5.viewNormal = (-0.595257, -0.536691, 0.598023)
v5.focus = (275.329, 29.2667, -7.50835)
v5.viewUp = (0.418228, 0.428551, 0.800893)
v5.viewAngle = 30
v5.parallelScale = 7.89321
v5.nearPlane = -15.7864
v5.farPlane = 15.7864
v5.imagePan = (0.0246213, -0.393998)
v5.imageZoom = 3.4
v5.perspective = 1
v5.eyeAngle = 2
v5.centerOfRotationSet = 0
v5.centerOfRotation = (275.329, 29.2667, -7.50835)
v5.axis3DScaleFlag = 0
v5.axis3DScales = (1, 1, 1)
v5.shear = (0, 0, 1)


v6 = View3DAttributes()
v6.viewNormal = (-0.573964, -0.421074, 0.702326)
v6.focus = (275.329, 29.2667, -7.50835)
v6.viewUp = (0.461805, 0.541829, 0.702252)
v6.viewAngle = 30
v6.parallelScale = 7.89321
v6.nearPlane = -15.7864
v6.farPlane = 15.7864
v6.imagePan = (-0.0221679, -0.356113)
v6.imageZoom = 2.97521
v6.perspective = 1
v6.eyeAngle = 2
v6.centerOfRotationSet = 0
v6.centerOfRotation = (275.329, 29.2667, -7.50835)
v6.axis3DScaleFlag = 0
v6.axis3DScales = (1, 1, 1)
v6.shear = (0, 0, 1)


time_views = (v2, v3, v4, v5, v6)


# Second loop for the pseudo color temp
size = len( time_views )
x_temp = []
for i in range( size ):
    x_temp += [float(i) / float( size-1 )]

slider = GetAnnotationObject( "Time" )
states = TimeSliderGetNStates()
for i in xrange( states ):
    SetTimeSliderState(i)
    slider.text = "Day = %d" % ( i/(states/31) )
    t = float(i) / float(states - 1)
    c = EvalCubicSpline(t, x_temp, time_views)  
    SetSaveWindowAttributes(s)
    SetView3D(c)
    SaveWindow()


