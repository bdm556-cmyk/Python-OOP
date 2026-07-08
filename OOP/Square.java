public class Square extends Shape {
    private int side;

    public Square(Coordinates coord, int side) {
        super(4, coord);
        this.side = side;
    }

    public double getArea() {
        return side * side;
    }

    public double getPerimeter() {
        return 4 * side;
    }

    public void scale(int factor, boolean sign) {
        super.scale(factor, sign);
        if (sign) {
            side = side * factor;
        } else {
            side = side / factor;
        }
    }

    public String display() {
        return "Square\n"
                + "Position: " + getCoordinates().display() + "\n"
                + "Side: " + side + "\n"
                + "Area: " + String.format("%.2f", getArea()) + "\n"
                + "Perimeter: " + String.format("%.2f", getPerimeter()) + "\n";
    }
}
