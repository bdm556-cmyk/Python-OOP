public class Circle extends Shape {
    private int radius;

    public Circle(Coordinates coord, int radius) {
        super(0, coord);
        this.radius = radius;
    }

    public double getArea() {
        return Math.PI * radius * radius;
    }

    public double getPerimeter() {
        return 2 * Math.PI * radius;
    }

    public void scale(int factor, boolean sign) {
        super.scale(factor, sign);
        if (sign) {
            radius = radius * factor;
        } else {
            radius = radius / factor;
        }
    }

    public String display() {
        return "Circle\n"
                + "Position: " + getCoordinates().display() + "\n"
                + "Radius: " + radius + "\n"
                + "Area: " + String.format("%.2f", getArea()) + "\n"
                + "Perimeter: " + String.format("%.2f", getPerimeter()) + "\n";
    }
}
