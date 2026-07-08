import java.util.ArrayList;

public class ShapeList {
    private ArrayList<Shape> listofShapes;

    public ShapeList() {
        listofShapes = new ArrayList<Shape>();
    }

    public void addShape(Shape s) {
        listofShapes.add(s);
    }

    public void translateShapes(int dx, int dy) {
        for (int i = 0; i < listofShapes.size(); i++) {
            listofShapes.get(i).translate(dx, dy);
        }
    }

    // Check the position before using the ArrayList.
    public Shape getShape(int pos) {
        if (pos >= 0 && pos < listofShapes.size()) {
            return listofShapes.get(pos);
        } else {
            System.out.println("No shape at position " + pos);
            return null;
        }
    }

    public Shape removeShape(int pos) {
        if (pos >= 0 && pos < listofShapes.size()) {
            return listofShapes.remove(pos);
        } else {
            System.out.println("No shape at position " + pos);
            return null;
        }
    }

    public double area(int pos) {
        Shape s = getShape(pos);
        if (s != null) {
            return s.getArea();
        } else {
            return 0.0;
        }
    }

    public void scale(int factor, boolean sign) {
        for (int i = 0; i < listofShapes.size(); i++) {
            listofShapes.get(i).scale(factor, sign);
        }
    }

    public double perimeter(int pos) {
        Shape s = getShape(pos);
        if (s != null) {
            return s.getPerimeter();
        } else {
            return 0.0;
        }
    }

    public int getNumberOfShapes() {
        return listofShapes.size();
    }

    public String display() {
        String output = "";
        if (listofShapes.size() == 0) {
            output = "No shapes in the list.\n";
        } else {
            for (int i = 0; i < listofShapes.size(); i++) {
                output = output + "Position " + i + ":\n";
                output = output + listofShapes.get(i).display() + "\n";
            }
        }
        return output;
    }
}
