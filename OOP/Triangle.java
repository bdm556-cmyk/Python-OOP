public class Triangle extends Shape {
    private Coordinates vertex2;
    private Coordinates vertex3;

    public Triangle(Coordinates vertex1, Coordinates vertex2, Coordinates vertex3) {
        super(3, vertex1);
        this.vertex2 = vertex2;
        this.vertex3 = vertex3;
    }

    public double getPerimeter() {
        double a = getCoordinates().distance(vertex2);
        double b = vertex2.distance(vertex3);
        double c = vertex3.distance(getCoordinates());
        return a + b + c;
    }

    // Heron's formula is used because the triangle is given by three vertices.
    public double getArea() {
        double a = getCoordinates().distance(vertex2);
        double b = vertex2.distance(vertex3);
        double c = vertex3.distance(getCoordinates());
        double s = (a + b + c) / 2;
        return Math.sqrt(s * (s - a) * (s - b) * (s - c));
    }

    // Triangle has three vertices, so all vertices must move together.
    public void translate(int dx, int dy) {
        super.translate(dx, dy);
        vertex2.translate(dx, dy);
        vertex3.translate(dx, dy);
    }

    public void scale(int factor, boolean sign) {
        super.scale(factor, sign);
        vertex2.scale(factor, sign);
        vertex3.scale(factor, sign);
    }

    public String display() {
        return "Triangle\n"
                + "Vertex 1: " + getCoordinates().display() + "\n"
                + "Vertex 2: " + vertex2.display() + "\n"
                + "Vertex 3: " + vertex3.display() + "\n"
                + "Area: " + String.format("%.2f", getArea()) + "\n"
                + "Perimeter: " + String.format("%.2f", getPerimeter()) + "\n";
    }
}
