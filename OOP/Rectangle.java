public class Rectangle extends Shape {
    private int width;
    private int length;

    public Rectangle(Coordinates coord, int width, int length) {
        super(4, coord);
        this.width = width;
        this.length = length;
    }

    public double getArea() {
        return width * length;
    }

    public double getPerimeter() {
        return (2 * width) + (2 * length);
    }

    public void scale(int factor, boolean sign) {
        super.scale(factor, sign);
        if (sign) {
            width = width * factor;
            length = length * factor;
        } else {
            width = width / factor;
            length = length / factor;
        }
    }

    public String display() {
        return "Rectangle\n"
                + "Position: " + getCoordinates().display() + "\n"
                + "Width: " + width + ", Length: " + length + "\n"
                + "Area: " + String.format("%.2f", getArea()) + "\n"
                + "Perimeter: " + String.format("%.2f", getPerimeter()) + "\n";
    }
}
