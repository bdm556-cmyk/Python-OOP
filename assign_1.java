abstract class Shape {
    private Coordinates position;
    private int sides;

    public Shape(int noOfSides, Coordinates coord) {
        this.sides = noOfSides;
        this.position = coord;
    }

    public Coordinates getCoordinates() {
        return position;
    }

    public int getSides() {
        return sides;
    }

    public void setCoordinates(Coordinates newcoord) {
        this.position = newcoord;
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

class Coordinates {
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

    public double distance(Coordinates p) {
        int xDifference = this.x - p.getX();
        int yDifference = this.y - p.getY();

        return Math.sqrt((xDifference * xDifference) + (yDifference * yDifference));
    }

    public void translate(int dx, int dy) {
        this.x = this.x + dx;
        this.y = this.y + dy;
    }

    public void scale(int factor, boolean sign) {
        if (factor <= 0) {
            System.out.println("Scale factor must be greater than 0.");
        } else {
            if (sign) {
                this.x = this.x * factor;
                this.y = this.y * factor;
            } else {
                this.x = this.x / factor;
                this.y = this.y / factor;
            }
        }
    }

    public String display() {
        return "X = " + x + ", Y = " + y;
    }
}

class Rectangle extends Shape {
    private int width;
    private int length;

    public Rectangle(Coordinates coord, int width, int length) {
        super(4, coord);
        this.width = width;
        this.length = length;
    }

    public int getWidth() {
        return width;
    }

    public int getLength() {
        return length;
    }


    public double getArea() {
        return width * length;
    }

    public double getPerimeter() {
        return (2 * width) + (2 * length);
    }

    public void scale(int factor, boolean sign) {
        super.scale(factor, sign);

        if (factor <= 0) {
            System.out.println("Scale factor must be greater than 0.");
        } else {
            if (sign) {
                width = width * factor;
                length = length * factor;
            } else {
                width = width / factor;
                length = length / factor;
            }
        }
    }

    public String display() {
        return "Rectangle\n"
                + "Position: " + getCoordinates().display() + "\n"
                + "Width: " + width + "\n"
                + "Length: " + length + "\n"
                + "Area: " + String.format("%.2f", getArea()) + "\n"
                + "Perimeter: " + String.format("%.2f", getPerimeter());
    }
}