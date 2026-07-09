import java.util.Scanner;

public class ShapeManagement {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        ShapeList shapes = new ShapeList();
        boolean running = true;

        // Main menu loop. It stops by changing running to false.
        while (running) {
            System.out.println("Shape Management Menu");
            System.out.println("1: add a shape");
            System.out.println("2: remove a shape by position");
            System.out.println("3: get information about a shape by position");
            System.out.println("4: area and perimeter of a shape by position");
            System.out.println("5: display information of all the shapes");
            System.out.println("6: translate all the shapes");
            System.out.println("7: scale all the shapes");
            System.out.println("0: quit program");
            System.out.print("Enter your choice: ");
            int choice = input.nextInt();

            switch (choice) {
                case 1:
                    System.out.println("1: Triangle");
                    System.out.println("2: Rectangle");
                    System.out.println("3: Circle");
                    System.out.println("4: Square");
                    System.out.print("Choose shape type: ");
                    int shapeType = input.nextInt();

                    if (shapeType == 1) {
                        System.out.print("Enter vertex 1 x: ");
                        int x1 = input.nextInt();
                        System.out.print("Enter vertex 1 y: ");
                        int y1 = input.nextInt();
                        System.out.print("Enter vertex 2 x: ");
                        int x2 = input.nextInt();
                        System.out.print("Enter vertex 2 y: ");
                        int y2 = input.nextInt();
                        System.out.print("Enter vertex 3 x: ");
                        int x3 = input.nextInt();
                        System.out.print("Enter vertex 3 y: ");
                        int y3 = input.nextInt();
                        shapes.addShape(new Triangle(new Coordinates(x1, y1), new Coordinates(x2, y2), new Coordinates(x3, y3)));
                        System.out.println("Triangle added.");
                    } else if (shapeType == 2) {
                        System.out.print("Enter x position: ");
                        int x = input.nextInt();
                        System.out.print("Enter y position: ");
                        int y = input.nextInt();
                        System.out.print("Enter width: ");
                        int width = input.nextInt();
                        System.out.print("Enter length: ");
                        int length = input.nextInt();
                        shapes.addShape(new Rectangle(new Coordinates(x, y), width, length));
                        System.out.println("Rectangle added.");
                    } else if (shapeType == 3) {
                        System.out.print("Enter x position: ");
                        int x = input.nextInt();
                        System.out.print("Enter y position: ");
                        int y = input.nextInt();
                        System.out.print("Enter radius: ");
                        int radius = input.nextInt();
                        shapes.addShape(new Circle(new Coordinates(x, y), radius));
                        System.out.println("Circle added.");
                    } else if (shapeType == 4) {
                        System.out.print("Enter x position: ");
                        int x = input.nextInt();
                        System.out.print("Enter y position: ");
                        int y = input.nextInt();
                        System.out.print("Enter side: ");
                        int side = input.nextInt();
                        shapes.addShape(new Square(new Coordinates(x, y), side));
                        System.out.println("Square added.");
                    } else {
                        System.out.println("Unknown shape type.");
                    }
                    break;

                case 2:
                    System.out.print("Enter position, starting from 0: ");
                    int removePos = input.nextInt();
                    Shape removed = shapes.removeShape(removePos);
                    if (removed != null) {
                        System.out.println("Shape removed.");
                    }
                    break;

                case 3:
                    System.out.print("Enter position, starting from 0: ");
                    int infoPos = input.nextInt();
                    Shape selectedShape = shapes.getShape(infoPos);
                    if (selectedShape != null) {
                        System.out.println(selectedShape.display());
                    }
                    break;

                case 4:
                    System.out.print("Enter position, starting from 0: ");
                    int areaPos = input.nextInt();
                    Shape areaShape = shapes.getShape(areaPos);
                    if (areaShape != null) {
                        System.out.println("Area: " + String.format("%.2f", shapes.area(areaPos)));
                        System.out.println("Perimeter: " + String.format("%.2f", shapes.perimeter(areaPos)));
                    }
                    break;

                case 5:
                    System.out.println(shapes.display());
                    break;

                case 6:
                    System.out.print("Enter x distance: ");
                    int dx = input.nextInt();
                    System.out.print("Enter y distance: ");
                    int dy = input.nextInt();
                    shapes.translateShapes(dx, dy);
                    System.out.println("All shapes translated.");
                    break;

                case 7:
                    System.out.print("Enter factor: ");
                    int factor = input.nextInt();
                    if (factor == 0) {
                        System.out.println("The factor cannot be 0.");
                    } else {
                        System.out.println("1: increase/multiply");
                        System.out.println("2: decrease/divide");
                        System.out.print("Choose scale option: ");
                        int scaleChoice = input.nextInt();
                        if (scaleChoice == 1) {
                            shapes.scale(factor, true);
                            System.out.println("All shapes scaled up.");
                        } else if (scaleChoice == 2) {
                            shapes.scale(factor, false);
                            System.out.println("All shapes scaled down.");
                        } else {
                            System.out.println("Unknown scale option.");
                        }
                    }
                    break;

                case 0:
                    running = false;
                    System.out.println("Program ended.");
                    break;

                default:
                    System.out.println("Unknown menu choice.");
                    break;
            }
            System.out.println();
        }

        input.close();
    }
}
