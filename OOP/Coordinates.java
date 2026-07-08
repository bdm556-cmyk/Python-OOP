public class Coordinates {
    private int x;
    private int y;

    public Coordinates(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    // Distance between this point and another point.
    public double distance(Coordinates p) {
        int xDifference = x - p.getX();
        int yDifference = y - p.getY();
        return Math.sqrt((xDifference * xDifference) + (yDifference * yDifference));
    }

    public void translate(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }

    public void scale(int factor, boolean sign) {
        if (sign) {
            x = x * factor;
            y = y * factor;
        } else {
            x = x / factor;
            y = y / factor;
        }
    }

    public String display() {
        return "X = " + x + ", Y = " + y;
    }
}
