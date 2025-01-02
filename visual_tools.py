# -*- coding: utf-8 -*-

import numpy as np
import vtk


def mkVtkIdList(it):
    vil = vtk.vtkIdList();
    for i in it:
        vil.InsertNextId(int(i));
    return vil;

class Visualization(object):
    """
    Clase Madre Visualization...
    """
    # Constructor de la clase
    def __init__(self, points):
        # We'll create the building blocks of polydata including data attributes.
        self._myPolygon = vtk.vtkPolyData();
        self._myPoints  = vtk.vtkPoints();
        self._myPolys   = vtk.vtkCellArray();
        self._myScalars = vtk.vtkFloatArray();
        self._myPolygonActor = vtk.vtkActor();
        self._myTextActor= vtk.vtkVectorText();
        self._textMapper = vtk.vtkPolyDataMapper();
        self._myTextActorFollower = vtk.vtkFollower()
        
  #Clase Texto      
class TextShow(Visualization):
    """
    Clase Polygon heredada de Visualization...
    """
    def __init__(self, text, size):
        # Llamo al constructor de Visualization
        Visualization.__init__(self, text);
        
        
        self._myTextActor.SetText("Origin")
        
        
        self._textMapper.SetInputConnection(self._myTextActor.GetOutputPort())
       
        self._myTextActorFollower.SetMapper(self._textMapper)
        self._myTextActorFollower.SetScale(10,10, 10)
        self._myTextActorFollower.AddPosition(0, -0.1, 0)

    
        
    def setColor(self, color):
        self._myTextActor.GetTextProperty().SetColor(color);
        
    def setPosition(self, position):
        self._myTextActor.SetDisplayPosition(position);

class Polygon(Visualization):
    """
    Clase Polygon heredada de Visualization...
    """
    def __init__(self, points, faces):
        # Llamo al constructor de Visualization
        Visualization.__init__(self, points);
        # Load the point, cell, and data attributes.
        for i in range(len(points)):
            self._myPoints.InsertPoint(i, points[i]);
            self._myScalars.InsertTuple1(i,i);
        for i in range(len(faces)):
            self._myPolys.InsertNextCell( mkVtkIdList(faces[i]) );
            
        # We now assign the pieces to the vtkPolyData.
        self._myPolygon.SetPoints(self._myPoints);
        self._myPolygon.SetPolys(self._myPolys);
        
        # Now we'll look at it.
        myPolygonMapper = vtk.vtkPolyDataMapper();
        if vtk.VTK_MAJOR_VERSION <= 5:
            myPolygonMapper.SetInput(self._myPolygon);
        else:
            myPolygonMapper.SetInputData(self._myPolygon);
        myPolygonMapper.SetScalarRange(0,len(points)-1);
        self._myPolygonActor.SetMapper(myPolygonMapper);
        
    def setOpacity(self, opacity):
        self._myPolygonActor.GetProperty().SetOpacity(opacity);
        
    def setColor(self, color):
        self._myPolygonActor.GetProperty().SetColor(color);
    
    def setJetScalar(self):
        self._myPolygon.GetPointData().SetScalars(self._myScalars);
        
# clase Línea
class Line(Visualization):
    """
    Clase Line heredada de Visualization...
    """
    def __init__(self, points):
        myLines = [];
        # Llamo al constructor de Visualization
        Visualization.__init__(self, points);
        # Load the point, cell, and data attributes.
        for i in range(len(points)):
            self._myPoints.InsertNextPoint(points[i]);
            self._myScalars.InsertTuple1(i,i);
        
        for i in range(len(points)-1):
            myLines.append(vtk.vtkLine());
            myLines[i].GetPointIds().SetId(0,i);
            myLines[i].GetPointIds().SetId(1,i+1);
            self._myPolys.InsertNextCell(myLines[i]);
        
        # We now assign the pieces to the vtkPolyData.
        self._myPolygon.SetPoints(self._myPoints);
        self._myPolygon.SetLines(self._myPolys);
        
        # Now we'll look at it.
        myPolygonMapper = vtk.vtkPolyDataMapper();
        if vtk.VTK_MAJOR_VERSION <= 5:
            myPolygonMapper.SetInput(self._myPolygon);
        else:
            myPolygonMapper.SetInputData(self._myPolygon);
        myPolygonMapper.SetScalarRange(0,len(points)-1);
        self._myPolygonActor.SetMapper(myPolygonMapper);
        
        self._myPolygonActor.GetProperty().SetLineWidth(1);
        
    def setOpacity(self, opacity):
        self._myPolygonActor.GetProperty().SetOpacity(opacity);
    
    def setColor(self, color):
        self._myPolygonActor.GetProperty().SetColor(color);
        
    def setJetScalar(self):
        self._myPolygon.GetPointData().SetScalars(self._myScalars);
        
# clase Puntos
class Points(Visualization):
    """
    Clase Points heredada de Visualization...
    """
    def __init__(self, listPoints):
        # Llamo al constructor de Visualization
        Visualization.__init__(self, listPoints);
        # Load the point, cell, and data attributes.
        self._myPolys.InsertNextCell(len(listPoints));
        for point in listPoints:
            ID = self._myPoints.InsertNextPoint(point);
            self._myPolys.InsertCellPoint(ID);
            
        # We now assign the pieces to the vtkPolyData.
        self._myPolygon.SetPoints(self._myPoints);
        self._myPolygon.SetVerts(self._myPolys);
        
        # Now we'll look at it.
        myPolygonMapper = vtk.vtkPolyDataMapper();
        if vtk.VTK_MAJOR_VERSION <= 5:
            myPolygonMapper.SetInput(self._myPolygon);
        else:
            myPolygonMapper.SetInputData(self._myPolygon);
        self._myPolygonActor.SetMapper(myPolygonMapper);
        
        self._myPolygonActor.GetProperty().SetPointSize(5); # tamaño del punto
        
    def setColor(self, color): # establece el color
        self._myPolygonActor.GetProperty().SetColor(color);
        
    def setOpacity(self, opacity):
        self._myPolygonActor.GetProperty().SetOpacity(opacity)
        
    def setPointSize(self, pointSize): # establece el tamaño del punto
        self._myPolygonActor.GetProperty().SetPointSize(pointSize);
    
# visualiza los actors
def showPolygons(Polygons):
    # The usual rendering stuff.
    camera = vtk.vtkCamera();
    camera.SetPosition(1,1,1);
    camera.SetFocalPoint(0,0,0);
     
    renderer = vtk.vtkRenderer();
    renWin   = vtk.vtkRenderWindow();
    renWin.AddRenderer(renderer);
     
    iren = vtk.vtkRenderWindowInteractor();
    iren.SetRenderWindow(renWin);
    
    for polygon in Polygons:
        renderer.AddActor(polygon._myPolygonActor);
    
    renderer.SetActiveCamera(camera);
    renderer.ResetCamera();
    renderer.SetBackground(1.,1.,1.);
    
    transform = vtk.vtkTransform();
    transform.Translate(0.0, 0.0, 0.0); # axis situado en el origen
    transform.Scale(20.0, 20.0, 20.0); # escala del axis
    

    renWin.SetSize(1440,900);
     
    # interact with data
    renWin.Render();
    iren.Start();
    
    

def visual_allpoints(all_points):
      
    myActors = [];

    for i in range(len(all_points)):
        for fiber in all_points[i]:
            body = Line(fiber);
            body.setJetScalar();
            myActors.append(body);    
    
    
    showPolygons(myActors);
    
def visual_centroids(cen_points):
        
    myActors = [];
    
    for i in range(len(cen_points)):

        body = Line(cen_points[i][0]);
        body.setJetScalar();
        myActors.append(body);    
    
    showPolygons(myActors);

def visual_region_by_list_all_fiber(mri_data, all_points, list_fiber_index, label_1, label_2 ):
    
    
    
    x1,y1, z1=np.where(mri_data==label_1)
    lista_point_1=[]
    for i in range (len(x1)):
        lista_point_1.append([x1[i], y1[i], z1[i]])
        
        
    x1,y1, z1=np.where(mri_data==label_2)
    lista_point_2=[]
    for i in range (len(x1)):
        lista_point_2.append([x1[i], y1[i], z1[i]])
    
    myActors = [];
    
    
    
    for i in list_fiber_index:#range(len(cen_points)):
        for fiber in all_points[i]:
            body = Line(fiber);
            body.setJetScalar();
            myActors.append(body);    
    
    pts_1= Points(lista_point_1)
    pts_1.setColor([1,0.5,0.7]);
    pts_1.setOpacity(0.07);
    pts_1.setPointSize(10);
    
    
    myActors.append(pts_1);
    
    pts_2= Points(lista_point_2)
    pts_2.setColor([0.5,0.5,1]);
    pts_2.setOpacity(0.07);
    pts_2.setPointSize(10);
    
    myActors.append(pts_2);
    
    showPolygons(myActors);
    

def visual_region_by_list(mri_data, cen_points, list_fiber_index, label_1, label_2 ):
    
    
    
    x1,y1, z1=np.where(mri_data==label_1)
    lista_point_1=[]
    for i in range (len(x1)):
        lista_point_1.append([x1[i], y1[i], z1[i]])
        
        
    x1,y1, z1=np.where(mri_data==label_2)
    lista_point_2=[]
    for i in range (len(x1)):
        lista_point_2.append([x1[i], y1[i], z1[i]])
    
    myActors = [];
    
    
    
    for i in list_fiber_index:#range(len(cen_points)):
        body = Line(cen_points[i][0]);
        body.setJetScalar();
        myActors.append(body);    
    
    pts_1= Points(lista_point_1)
    pts_1.setColor([1,0.5,0.7]);
    pts_1.setOpacity(0.07);
    pts_1.setPointSize(10);
    
    
    myActors.append(pts_1);
    
    pts_2= Points(lista_point_2)
    pts_2.setColor([0.5,0.5,1]);
    pts_2.setOpacity(0.07);
    pts_2.setPointSize(10);
    
    myActors.append(pts_2);
    
    showPolygons(myActors);

def visual_region(mri_data, cen_points, label_1, label_2):
    
        
    x1,y1, z1=np.where(mri_data==label_1)
    lista_point_1=[]
    for i in range (len(x1)):
        lista_point_1.append([x1[i], y1[i], z1[i]])
        
        
    x1,y1, z1=np.where(mri_data==label_2)
    lista_point_2=[]
    for i in range (len(x1)):
        lista_point_2.append([x1[i], y1[i], z1[i]])
    
    myActors = [];
    
    
    
    for i in range(len(cen_points)):
        body = Line(cen_points[i][0]);
        body.setJetScalar();
        myActors.append(body);    
    
    pts_1= Points(lista_point_1)
    pts_1.setColor([1,0.5,0.7]);
    pts_1.setOpacity(0.07);
    pts_1.setPointSize(10);
    
    
    myActors.append(pts_1);
    
    pts_2= Points(lista_point_2)
    pts_2.setColor([0.5,0.5,1]);
    pts_2.setOpacity(0.07);
    pts_2.setPointSize(10);
    
    myActors.append(pts_2);
    
    showPolygons(myActors);



def visual_all_mri(mri_data, cen_points):
    
    x1,y1, z1=np.where(mri_data!=0)
    lista_point_1=[]
    for i in range (len(x1)):
        lista_point_1.append([x1[i], y1[i], z1[i]])
    

    
    myActors = [];
    
    
    
    for i in range(len(cen_points)):
        body = Line(cen_points[i][0]);
        body.setJetScalar();
        myActors.append(body);    
    
    pts_1= Points(lista_point_1)
    pts_1.setColor([1,0.5,0.7]);
    pts_1.setOpacity(0.07);
    pts_1.setPointSize(10);
    
    
    myActors.append(pts_1);
    
    
    showPolygons(myActors);


def reorient_nibabel_image_DSI_no_interp(mri_):
    
    """Corrección de las coordenadas para la imagen anatómica  y,z,x = x,y,z"""

    mri_data = mri_.get_data()
    
    y1,z1, x1=np.where(mri_data!=0)
    
    z2=-1*z1
    z2=z2 + mri_data.shape[1]
  
    x2=-1*x1                  
    x2=x2 + mri_data.shape[2]
  
    y2=y1

    
    new_mri = np.zeros([np.int(mri_data.shape[2]),np.int(mri_data.shape[0]),np.int(mri_data.shape[1])])
    
    
    
    for i in range (len(x1)):
        atlas_value = mri_data[y1[i],z1[i], x1[i]]
        new_mri[np.int(x2[i]), np.int(y2[i]), np.int(z2[i])] = atlas_value
             
    
    return new_mri
    
    