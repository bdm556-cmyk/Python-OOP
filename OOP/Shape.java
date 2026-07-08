public abstract class Shape {
    private Coordinates position;
    private int sides;

    public Shape(int noOfSides, Coordinates coord) {
        sides = noOfSides;
        position = coord;
    }

    public Coordinates getCoordinates() {
        return position;
    }

    public int getSides() {
        return sides;
    }

    public void setCoordinates(Coordinates newcoord) {
        position = newcoord;
    }

    public void translate(int dx, int dy) {
        position.translate(dx, dy);
    }

    public void scale(int factor, boolean sign) {
        position.scale(factor, sign);
    }

    public abstract double getArea();

    public abstract double getPerimeter();

    public abstract String display();
}
